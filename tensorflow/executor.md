Tensorflow Graph Executor(草稿)
-------------------------
## 摘要

Tensorflow中单机版的(direct session)会按照device将graph先划分成子图subgraph, 然后每个subgraph会交给一个execturo去执行，分布式的（GrpSession) 首先会将graph按照worker划分，每个worker划分成一个子图，然后注册到每个worker的graph_mgr, 并在graph_mgr中再按照device将worker_subgraph划分成device的subgraph, 最后每个device对应的subgraph会由executor去执行，Tensorflow中的graph执行示意图如下(图片来自[tensorflow-talk-debugging](https://wookayin.github.io/tensorflow-talk-debugging/#1))。

![tensors_flowing](./images/tensors_flowing.gif)

本文主要分析了executor在执行graph时，Node的执行调度以及node的输入输出数据, 执行状态是如何保存的，最后结合代码和[Tensorflow control flow implemention](http://download.tensorflow.org/paper/white_paper_tf_control_flow_implementation_2017_11_1.pdf)这部分文档分析了的control flow的具体实现。主要涉及的代码为common_runtime/executor.cc

### Executor中主要类

#### Executor 
Executor为基类，对外提供了两个接口Run和RunAsync, 其中Run是对RunAsync简单的一层包装。

```cpp

  // Synchronous wrapper for RunAsync().
  Status Run(const Args& args) {
    Status ret;
    Notification n;
    RunAsync(args, [&ret, &n](const Status& s) {
      ret = s;
      n.Notify();
    });
    n.WaitForNotification();
    return ret;
  }
```

Executor基类只要去实现RunAsync就行。
```cpp
  virtual void RunAsync(const Args& args, DoneCallback done) = 0;
```

#### ExecutorImpl

ExecutorImpl继承实现了Executor，它的RunAsync实现转发给了ExecutorState::RunAsync, ExecutorImpl主要的工作是从Graph中解析出一些静态信息，比如FrameInfo, GraphView, 由后面的ExecutorState执行的时候使用。

~~~cpp
void ExecutorImpl::RunAsync(const Args& args, DoneCallback done) {
  (new ExecutorState(args, this))->RunAsync(std::move(done));
}
~~~

#### ExecutorState





### Executor中的调用关系

### ExecutorImpl call flow

Executor被调用的入口为NewLocalExecutor, 在DirectSesion中会为每个subgraph创建一个executor, 然后交给ExecutorBarrier同时执行多个Executor。NewLocalExecutor在ExecutorImpl成员函数中的调用过程如下：

![executor impl call flow](./images/executor_impl_call.jpeg)

Exector::RunAsync这个会被转发给ExecutorState::RunAsync（这个函数的执行逻辑见下文）

### ExecutorImpl::Initialize

在ExecutorImpl::Initialize中，对于graph中的每个node, 创建对应的NodeItem, 主要包含了三块：

1. 调用params.create_kernal, 创建nodeItem->kernal.
2. 记录nodeItem.input_start, input_start 是该node在它所属frame的input_tensors中的偏移index, 这个在后面的ProcessInputs和ProcessOutputs中会用到。
3. 创建node对应的pending_id， pending_id用于找到记录它执行状态的pendingCount, 这个在后面的ActiveNode中会用到.

在BuildCtronlFlow中会建立好framename之间的父子关系, frameInfo是frame的静态信息（对应着执行时候的FrameState动态信息），并且建立了从node id找到node所属frame name的映射关系，包含了frame中的total inputs, 这个frame所包含的node.

![image](./images/tf-executor-init.jpeg)

## ExecutorState::RunAsync

![image](./images/tf-executor-call-flow.jpeg)


### ExecutorImpl::Process

![image](./images/tf-executor-data-flow.jpeg)


## Control Flow


后来在[1]中发现节点还有Switch, Merge, IterNext, Enter, Exit 五个flow control node，用来实现while循环，为此tensorflowe引入了frame的概念，可以粗略的认为和函数调用一样吧, 在遇到Enter node的时候，就新建一个child frame，把inputs(类似于函数函数调用时候参数入栈)一样，forward到child frame中，在遇到Exit node，就把输出放到parent frame 中(类似于将函数的return值入栈)。

未完待续

## Executor中数据流程

## 参考

1. [Tensorflow control flow implemention]
2. [tensorflow-talk-debugging](https://wookayin.github.io/tensorflow-talk-debugging/#1)
