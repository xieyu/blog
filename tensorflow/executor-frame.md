## Executor Frame


Frame存放node之间输入输出的tensor(具体的由Entry来实现)，以及node在frame中的执行状态(由PendingCount来实现)。FrameInfo包含了Graph的静态信息，
FrameState对应着一个while loop， IterationState则对应着while loop中的某个iter迭代时候的状态。
 IterationState中有个EntryVec用于保存某次迭代时候，node之间输入输出的Entry, 在分析executor中Frame相关代码之前，我们先看下tensorflow中的control flow op。



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

