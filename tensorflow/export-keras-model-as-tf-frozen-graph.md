## 将keras模型导出为tf frozen graph

#### frozen keras model

将keras的h5文件转换为tensorflow的pb文件,  这里面使用了 ``convert_variables_to_constants``将模型中的变量都convert成了常量（方便后续采用quantilize或者tensorrt， 对模型推断部分做进一步的优化）

```python
import keras
from keras.layers.core import K
import tensorflow as tf

def frozen_keras_model(keras_model_path, output_node_names, export_path):
    output_node_namess = output_nodes.split(",")
    model = keras.models.load_model(keras_model_path)
    print("the model output nodes is {}".format(model.outputs))
    with K.get_session() as sess:
        output_graph_def = tf.graph_util.convert_variables_to_constants(
            sess,
            tf.get_default_graph().as_graph_def(),
            output_nodes_names,
            variable_names_blacklist=['global_step']
        )
        with tf.gfile.Gfile(export_path, "wb") as f:
            f.write(output_graph_def.SerializeToString())
    
```

将``global_step``放到``variable_names_blacklist``是因为2中的bug.

```python
    variable_names_blacklist=['global_step']
```

可以通过print ``model.outputs``来查看keras的输出节点，可以通过tensorboard来看keras模型，然后找到最后的输出节点。一般keras模型的输出节点有好多个（比如训练用的之类的)，预测输出节点为其中的一个。

#### 使用tensorboard展示keras model对应的graph

首先使用tf summary创建相应的log

```python
def keras_model_graph(keras_model_path, log_dir):
    model = keras.model.load_model(keras_model_path)
    with K.get_session() as sess:
        train_writer = tf.summary.FileWriter(log_dir)
        train_writer.add_graph(sess.graph)
```

启动tensorboard

```
$tensorboard --log_dir logdir
```


### 参考文献

1. [Stackoverflow: How to export Keras .h5 to tensorflow .pb](https://stackoverflow.com/questions/45466020/how-to-export-keras-h5-to-tensorflow-pb?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa)

2. [BUG: freeze_graph producing invalid graph_def in tensorflow ](https://github.com/tensorflow/tensorflow/issues/14452)
