## Executor Frame


Frame存放node之间输入输出的tensor(由Entry来处理)，以及node在frame中的执行状态(由PendingCount来处理)。FrameInfo是静态信息。

对于Graph中的每个node都会属于某个Frame。由于tensorflow的graph可以实现while循环，while中的iteration也有独立的state.

### FrameInfo

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

FrameInfo包含的字段如下:

```
    // The total number of inputs to a frame.
    int input_count;

    // The total number of input tensors of a frame.
    // == sum(nodes[*].num_inputs()) where nodes are the nodes in the frame.
    int total_inputs;

    // Used to determine the next place to allocate space in the
    // pending_counts data structure we'll eventually construct
    PendingCounts::Layout pending_counts_layout;

    // Each frame has its own PendingCounts only for the nodes in the frame.
    PendingCounts* pending_counts;  // Owned

    // The nodes in a frame. Used only for debugging.
    std::vector<const Node*>* nodes;  // Owned
```

1. pending_counts_layout在后面会用来创建Node的PendingCount, pending count会用来跟踪Node的状态（比如是否所有的input都已ready, Node是否已经执行过了，Node是否在Dead path)，

2. total_inputs会在ExecutorState::IteratorState中用到，用于创建InputTensors数组。


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

