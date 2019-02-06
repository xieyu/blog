# Executor Frame

## 引言

在Executor 执行Graph的时候，会首先分析Graph, 创建关于Graph中frame的静态信息，比如ControlFlowInfo和FrameInfo，对于graph中的每个node, 可以根据ControlFlowInfo去得到它对应的frame_name, 然后根据frame_name可以得到FrameInfo的一些信息。

而FrameState和IterationState这两个是动态的状态，由Executor在执行Graph时候动态创建的。FrameState对应着整个while loop，而IterationState则对应着while loop中的某个迭代。 FrameState中包了total_input(frame中所有node input个数等信息），IterationState中有个EntryVec用于保存某次迭代时候，node之间输入输出的Entry。

本文主要分析了Executor中ControlFlowInfo， FrameInfo, FrameState, IterationState，这几个和Executor Frame相关的struct， 以及它们之间的关系。


## ExecutorImpl::ControlFlowInfo

ControlFlowInfo里面``unique_frame_names``保存了computation graph中所有frame的名字，frame_names则是个倒查表，索引对应于``node->id``, 可以根据``frame_names[node->id()]``找到node对应的frame_name.

```cpp
struct ControlFlowInfo {
  gtl::FlatSet<string> unique_frame_names;
  std::vector<string> frame_names;
};
```


### ControlFlowInfo的创建

BuildControlFlowInfo 会遍历整个graph, 然后处理Enter/Exit node, 填充好ControlFlowInfo中的字段, 

1. 如果遇到Enter node, 则进入子Frame, Enter node的每个输出node对应的frame_name都是EnterNode对应的 "frame_node"属性

```cpp
//Enter node包含了frame_name 属性，
GetNodeAttr(curr_node->attrs(), "frame_name", &frame_name));
```

2. 如果是Exit node, 则退出子Frame, Exit node的每个输出node对应的frame_name都是Exit node parent node的 frame_name

```cpp
//other code
else if (IsExit(curr_node)) {
    parent = parent_nodes[curr_id];
    frame_name = cf_info->frame_names[parent->id()];
    parent = parent_nodes[parent->id()];
}
```

3. 如果是其他类型的node, 则node的每个输出node frame和当前node一致

```cpp
 parent = parent_nodes[curr_id];
 frame_name = cf_info->frame_names[curr_id];
```

#### controlflow info被用到的地方

在executor中首先会根据node->id找到frame_name, 然后根据frame_name找到对应的FrameInfo
```cpp
    const string& frame_name = cf_info.frame_names[id];
    FrameInfo* frame_info = EnsureFrameInfo(frame_name);
```

## ExecutorImpl::FrameInfo

FrameInfo包含的主要字段如下:

```cpp
    // The total number of inputs to a frame.
    int input_count;

    int total_inputs;

    PendingCounts::Layout pending_counts_layout;
    PendingCounts* pending_counts;  // Owned
```
### input_count

input_count 代表graph中Enter到该frame的Enter Node个数, 统计个数的代码如下：

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


### total_inputs

total_inputs会在ExecutorState::IteratorState中用到，它的值为frame中所有node的inputs个数的总和。

```cpp
// The total number of input tensors of a frame.
// == sum(nodes[*].num_inputs()) where nodes are the nodes in the frame.
int total_inputs;
```

total_inputs在后面的影响如下：
```
FrameInfo.total_inputs ==> FrameState.total_input_tensors ==> IterationsState.input_tensors(new Entry[total_input_tensors])
```

### PendingCounts

3. PendingCounts相关，pending_counts_layout在后面会用来创建Node的PendingCount, pending count会用来跟踪Node的状态（比如是否所有的input都已ready, Node是否已经执行过了，Node是否在Dead path)，

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
FrameInfo将在ExecutorImpl的析构函数中被删掉。
```cpp
  ~ExecutorImpl() override {
    //other code
    for (auto fiter : frame_info_) {
      delete fiter.second;
    }
```

## ExecutorState::FrameState

前面两个ControlFlowInfo/FrameInfo都是静态的信息(所以叫XXXInfo)，而FrameState和IterationState都是动态信息，会在Graph执行的时候动态创建。

#### 创建FrameState: FindOrCreateChildFrame

在FindOrCreateChildFrame中，会调用InitializeFrameInfo从FrameInfo中抽取有用的字段
```cpp
    void InitializeFrameInfo(const string& enter_name) {
      auto it_frame_info = executor->frame_info_.find(enter_name);
      DCHECK(it_frame_info != executor->frame_info_.end());
      ExecutorImpl::FrameInfo* finfo = it_frame_info->second;
      pending_counts = finfo->pending_counts;
      total_input_tensors = finfo->total_inputs;
      num_pending_inputs = finfo->input_count;
      nodes = finfo->nodes;
    }
```

FindOrCreateChildFrame被调用的stack
```
Process -> PropagationOutputs -> FindOrCreateChildFrame
```


### 删除FrameState: DeleteFrame

1.在PropgateOutputs中，如果is_frame_done，就会调用DeleteFrame, DeleteFrame会向parent frame传播dead_exits（TODO: 这部分描述细化）

IterationState删除的地方

1. CleanupFrameIterations
2. frame->CleanupIterations


## ExecutorState::IterationState

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

