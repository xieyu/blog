## 使用dataset iterator 优化keras model预测的吞吐量


### predict_on_generator

现在做的项目，需要在短时间内一次性预测一组大量的图片，刚开始的时候，采用了keras的predict_on_generator和Sequnce，速度比一个个feed dict的形式快了不少, 但是吞吐量还是没达到要求，感觉还有优化的地方。

```python
class BatchSequnce(Sequence):
    def __len__(self):
        # 返回batch总个数
        return self.batch_count

    def __getitem__(self, idx):
        #返回一个batch的数据
        #这里可能会做一些数据预处理的工作，比如将图片从文件中加载到内存中然后做特征预处理
        pass
```

```python
 model = keras.load_model(model_path)
 generator = BatchSequnce(....)
 ret = model.predict_generator(
         generator=generator,
         steps=None,
         workers=10,
         verbose=True,
 )
```


### Dataset

经分析, GPU每次都要等 BatchSequnce的``__getitem___``处理完之后，才能fetch到数据，如果``__getitem__``做了比较耗时间的操作的话，会让GPU一直在等待, 而且GPU在处理每个Batch数据的时候，都要等一次, tensorflow的Prefech感觉可以缓解这个问题，后来尝试了下，所消耗的时间优化到了以前的70%左右。

#### 使用iterator 改造keras模型

1. 首先采用[将keras模型导出为tf frozen graph](./export-keras-model-as-tf-frozen-graph.md)中的方式，将Keras的h5模型转换成tensorflow的pb文件。

2. 使用``tf.data.Iterator.from_structure``(可重新初始化迭代器可以通过多个不同的 Dataset 对象进行初始)的形式, 声明iterator的输出dtype和TensorShape,

3. 调用``tf.import_graph_def`` 导入模型, 导入的时候，使用input_map将placeholde,比如"input"替换成Dataset的itereator next_element


这部分代码如下

```python
    def load_model(self, sess, frozen_model_file):
        with tf.name_scope("dataset"):
            iterator = tf.data.Iterator.from_structure(
                    tf.float32,
                    tf.TensorShape([self.batch_size, 450, 450, 3]))
            next_element = iterator.get_next()
            next_element = tf.convert_to_tensor(next_element, tf.float32)

        with tf.gfile.GFile(frozen_model_file, "rb") as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        tf.import_graph_def(
                graph_def,
                name="",
                input_map={"input_1:0": next_element})
        output_op_name = "y"
        output_op = sess.graph.get_operation_by_name(output_op_name).outputs[0]
        return iterator, output_op
```

### 设计DataSet

这里面需要注意的时候, 真正的map函数需要采用py_func包一层, 同事指定py_func的输出tensor shape, 这里的num_map_parall一般取cpu的个数.

```python
class DataSetFactory(object):
    def make_dataset(self):
        def generator():
            #返回要处理的文件路径, 或者坐标等
            yield [x, y, w, h]

        output_types = (tf.float32)
        output_shapes = (tf.TensorShape([4]))
        ds = tf.data.Dataset.from_generator(
                generator,
                output_types,
                output_shapes=output_shapes)

        ds = ds.map(lambda region: self.map_func(region), num_map_parall=80)

        ds = ds.prefetch(buffer_size=self.batch_size * 256)
        ds = ds.batch(self.batch_size)
        ds = ds.prefetch(buffer_size=self.batch_size * 10)

        return ds

    def map_func(self, region):
        def do_map(region):
            # 加载图片和预处理
            return img_data
        # 这里采用了py_func，可以执行任意的Python函数，同时需要后面通过reshape的方式设置
        # image_data的shape。
        img_data = tf.py_func(do_map, [region], [tf.float64])
        img_data = tf.reshape(img_data, [450, 450, 3])
        img_data = tf.cast(img_data, tf.float32)
        return image_data
```

#### prefetch_to_device

tensorflow 后来加了prefetch_to_device, 经测试可以提高5%左右的效率吧,但是和structure iterator初始化的时候有冲突，因此这个地方把它去掉了。
```python
# 由于prefech_to_device必须是dataset的最后一个处理单元，
# structure iterator用这个ds初始化的时候会有问题，
# 因此这个地方将prefetch_to_gpu注释掉了
# gpu_prefetch = tf.contrib.data.prefetch_to_device(
#         "/device:GPU:0",
#         buffer_size=self.batch_size * 10)
# ds = ds.apply(gpu_prefetch)
```


#### 使用dataset初始化iterator

```python
    def init_iterator(self, dataset):
        # 这里的output_op就是load_model时返回的iterator
        init_iterator_op = self.iterator.make_initializer(dataset)
        self.sess.run(init_iterator_op)

    def predict(self):
        # 这里的output_op就是load_model时返回的output_op
        while True:
            outputs = self.sess.run(self.output_op)
```
