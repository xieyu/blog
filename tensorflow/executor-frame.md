## Executor Frame


Frame存放node之间输入输出的tensor(具体的由Entry来实现)，以及node在frame中的执行状态(由PendingCount来实现)。FrameInfo包含了Graph的静态信息，
FrameState对应着一个while loop， IterationState则对应着while loop中的某个iter迭代时候的状态。
 IterationState中有个EntryVec用于保存某次迭代时候，node之间输入输出的Entry, 在分析executor中Frame相关代码之前，我们先看下tensorflow中的control flow op。

### Tensorflow中的control flow op

本节主要参照 [Tensorflow control flow implemention](http://download.tensorflow.org/paper/white_paper_tf_control_flow_implementation_2017_11_1.pdf) 这篇文章。Tensorflow中control flow op主要包含以下几种:
在Tensorflow中，graph中每个node的op，都在一个execution Frame中执行，下面这几种control-flow op用于创建和管理这些execution Frame.


* <b>Switch</b>:  A Switch operator forwards the input tensor d to one of its outputs depending on the
boolean tensor of the control input p. A Switch is enabled for execution when both its inputs are
available.

* <b>Merge</b>:A Merge operator forwards one of its available inputs to its output. A Merge is enabled
for execution when any of its inputs is available. It is unspecified which available input it outputs
if there are multiple inputs available

* <b>Enter</b>: An Enter operator forwards its input to the execution frame that is uniquely
identified by the given name. This Enter op is used to pass a tensor in one execution frame to a
child execution frame. There can be multiple Enter ops to the same child execution frame, each
making a tensor available (asynchronously) in that child execution frame. An Enter is enabled
for execution when its input is available. A new execution frame is instantiated in the
TensorFlow runtime when the first Enter op to that frame is executed

* <b>Exit</b>: An Exit operator forwards a value from an execution frame to its parent execution frame.
This Exit op is used to return a tensor computed in a child execution frame back to its parent
frame. There can be multiple Exit ops to the parent frame, each asynchronously passing a
tensor back to the parent frame. An Exit is enabled when its input is available.

* <b>NextIteration</b>: A NextIteration operator forwards its input to the next iteration in the current
execution frame. The TensorFlow runtime keeps track of iterations in an execution frame. Any
op executed in an execution frame has a unique iteration id, which allows us to uniquely identify
different invocations of the same op in an iterative computation. Note that there can be multiple
NextIteration ops in an execution frame. The TensorFlow runtime starts iteration N+1 when the
first NextIteration op is executed at iteration N. As more tensors enter an iteration by executing
NextIteration ops, more ops in that iteration will be ready for execution. A NextIteration is
enabled when its input is available.

如果把execution frame和函数调用做类比的话，那么Enter有点类似于传参，而Exit则类似于return 返回值。


### ExecutorImpl::FrameInfo

FrameInfo包含的主要字段如下:

1. input_count

```cpp
    // The total number of inputs to a frame.
    int input_count;
```
在tensorflow中Enter类型的节点代表进入某个frame[]().
input_count初始化的地方如下, 会遍历整个graph中的node, 如果node是Enter类型节点的话，就把node->frame_name对应的frame 的input_count + 1。

```cpp
//ExecutorImpl::Initialize
  for (const Node* n : graph_->nodes()) {
    //other code..

    if (IsEnter(n)) {
      string enter_name;
      TF_RETURN_IF_ERROR(GetNodeAttr(n->attrs(), "frame_name", &enter_name));
      EnsureFrameInfo(enter_name)->input_count++;
    }
  }
```

2. total_inputs

total_inputs会在ExecutorState::IteratorState中用到，用于创建InputTensors数组。

```cpp
    // The total number of input tensors of a frame.
    // == sum(nodes[*].num_inputs()) where nodes are the nodes in the frame.
    int total_inputs;
```
3. PendingCounts相关

 pending_counts_layout在后面会用来创建Node的PendingCount, pending count会用来跟踪Node的状态（比如是否所有的input都已ready, Node是否已经执行过了，Node是否在Dead path)，
```cpp
    // Used to determine the next place to allocate space in the
    // pending_counts data structure we'll eventually construct
    PendingCounts::Layout pending_counts_layout;

    // Each frame has its own PendingCounts only for the nodes in the frame.
    PendingCounts* pending_counts;  // Owned
```



struct FrameInfo由EnsureFrameInfo这个函数lazy创建，并在Intialize填充好它的字段。

```cpp
  FrameInfo* EnsureFrameInfo(const string& fname) {
    auto slot = &frame_info_[fname];
    if (*slot == nullptr) {
      *slot = new FrameInfo;
    }
    return *slot;
  }
```

### ExecutorState::FrameState


#### FrameState删除的地方

1.在PropgateOutputs中，如果is_frame_done，就会调用DeleteFrame, DeleteFrame会向parent frame传播dead_exits（TODO: 这部分描述细化）

IterationState删除的地方

1. CleanupFrameIterations
2. frame->CleanupIterations


### IterationState

```cpp
    Entry* input_tensors;
    // The number of outstanding ops for each iteration.
    size_t outstanding_ops;
    int outstanding_frame_count;
    PendingCounts counts_;
```

###### FrameState和IterationState创建地方:

1. 在ExecutorState的构造函数中会创建一个FrameState作为rootframe, 同时也会创建该frameState的第一个IterationState。

2. 在执行完一个Node之后，PropagateOutputs在遇到Enter节点的时候，会调用FindOrCreateChildFrame来创建一个新的FrameState,以及该FrameState的第一个IterationState

3. 在PropgateOutputs的时候，遇到NextIteration Node 会去调用FrameState::IncreatementIteration新增一个IterationState

4. 所有的framesate都放在了outstanding_frames 这个map中，新建的framestate会插到这个map中，删除的时候会从这个map中去掉。


参考文献：

1. [Tensorflow control flow implemention](http://download.tensorflow.org/paper/white_paper_tf_control_flow_implementation_2017_11_1.pdf)
