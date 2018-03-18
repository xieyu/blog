Tensorflow Graph Executor
-------------------------
## 摘要

tensorflow中图的执行有单机版的(direct session)和分布式版的，两者最后都会用executor去执行图。本文主要分析了tensorflow 在执行computation graph中的调度逻辑，以及在执行graph过程中，node的输入输出数据，node的执行状态是怎么保存的。

在读这部分代码的时候，我想如果自己从头写这部分代码的话，需要解决那些问题，然后列了下面几个基本的问题

1. 怎么更新判断某个node是否可以执行的？
2. 每个node的输出放在哪儿，节点的输入去哪儿取？
3. 最开始从哪些节点开始执行？怎么样才算整个图执行完成了？
4. node之间如何并行地执行？

后来在[1]中发现节点还有Switch, Merge, IterNext, Enter, Exit 五个flow control node，用来实现while循环，为此tensorflowe引入了frame的概念，可以粗略的认为和函数调用一样吧, 在遇到Enter node的时候，就新建一个child frame，把inputs(类似于函数函数调用时候参数入栈)一样，forward到child frame中，在遇到Exit node，就把输出放到parent frame 中(类似于将函数的return值入栈)。

## Executor中数据流程

### ExecutorImpl::Initialize

在ExecutorImpl::Initialize中，对于graph中的每个node, 创建对应的NodeItem, 主要包含了三块：

1. 调用params.create_kernal, 创建nodeItem->kernal.
2. 记录nodeItem.input_start, input_start 是该node在它所属frame的input_tensors中的偏移index, 这个在后面的ProcessInputs和ProcessOutputs中会用到。
3. 创建node对应的pending_id， pending_id用于找到记录它执行状态的pendingCount, 这个在后面的ActiveNode中会用到.

在BuildCtronlFlow中会建立好framename之间的父子关系, frameInfo是frame的静态信息（对应着执行时候的FrameState动态信息），并且建立了从node id找到node所属frame name的映射关系，包含了frame中的total inputs, 这个frame所包含的node.

![image](./images/tf-executor-init.jpeg)

### ExecutorImpl::Process

![image](./images/tf-executor-data-flow.jpeg)


## ExecutorImpl::RunAsync

![image](./images/tf-executor-call-flow.jpeg)

## Control Flow

未完待续

## 参考

1. [Tensorflow control flow implemention]
