## Codes

### React
1.  [从jsx到html dom的流程分析](./React/from-jsx-to-dom.md)

### pthread
1. [Pthread Primer笔记](./Concurrency/pthread/pthread-primer.md)
2. [Pthread线程生命周期](./Concurrency/pthread/glibc-pthread-implement-thread-life-cycle.md)
3. [Pthread线程同步](./Concurrency/pthread/glibc-pthread-implement-sync.md)

###  hotspot

1. [osx下编译调试hotspot](./Java/hotspot-debug-under-osx.md)
2. [jvm的初始化时创建的线程](./Java/hotspot-thread-created-when-init.md)
3. [class文件的加载和执行](./Java/hotspot-class-file-load-and-run.md)

### tensorflow

1. [Executor: 执行Computation Sub Graph](./tensorflow/executor.md)
    - [SubGraph预处理：Node/NodeItem/TaggedNode](./tensorflow/executor-subgraph-preprocess.md)
    - [Flow control op: switch/merge/enter/exit/nextIteration](./tensorflow/flow-control-op.md)
    - [Frame: ControlFlowInfo/FrameInfo/FrameState/IterationState](./tensorflow/executor-frame.md)
    - Entry: 保存node之间的输入输出tensor
    - Pending Count: node执行状态
    - Execute Graph Computation: PrepareInputs/Process/ProcessOutputs/PropateOutputs

2. [DirectSession: 单机执行computation graph](./tensorflow/direct-session.md)
    - SessionFactory
    - Rewrite Graph
    - CallFrame: Feed and Fetch
    - Place node to device
    - Graph Partition
    - Create executors
    - Tensor Store

3. [RendezVous：跨设备，跨主机通信](./tensorflow/rendezvous.md)
    - Rendezvous主要模块以及继承关系
    - LocalRendezvous
    - IntraProcessRendezvous
    - CopyTensor::ViaDMA: GPU,CPU之间的通信
    - BaseRemoteRendezvous
    - RpcRemoteRenddezvous
    - RendezvousMgr

4. [Device：计算单元抽象(CPU/GPU)](./tensorflow/device.md)
    - Device继承关系
    - Device Factory
    - Device Thread pool
    - Device Context
    - Device Allocator

5. OpKernal Context
6. Opkernal
    - Variable
    - Const
    - PlaceHolder
    - Matmul
    - Conv

7. GrpSession: Grp分布式执行computation graph
8. Estimator
9. Dataset
10. tfslim


## Notes

1. keras模型部署优化
    - [将keras模型导出为tf frozen graph](./tensorflow/export-keras-model-as-tf-frozen-graph.md)
    - [使用dataset iterator 优化keras model预测的吞吐量](./tensorflow/replace-placeholder-with-iterator.md)



## 其他

1. [Redis in Action笔记](./Redis/redis-in-action-notes.md)
2. [Mysql cookbook笔记](./Mysql/mysql-cook-book-notes.md)
3. [docker学习笔记1： docker基本使用方法](./Docker/docker-basic-note.md)
4. [xv6 内存管理](./Os/xv6/memory.md)
