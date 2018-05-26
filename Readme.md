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

1. [Executor: 执行Computation Graph](./tensorflow/executor.md)
    - Graph预处理：Subgraph rewrite graph
    - Graph预处理：GraphView
    - Pending Count: 节点的执行状态
    - Execute Graph Computation: Graph执行的调度。
    - Flow Control Node: Switch/Merge/Exit/Enter/NextIter
    - FrameInfo, WhileLoop iter

2. [DirectSession: 单机执行computation graph](./tensorflow/direct-session.md)
3. [RendezVous：跨设备，跨主机通信](./tensorflow/rendezvous.md)
4. [Device：计算单元抽象(CPU/GPU)](./tensorflow/device.md)


## Notes

1. keras模型部署优化
    - [将keras模型导出为tf frozen graph](./tensorflow/export-keras-model-as-tf-frozen-graph.md)
    - [使用dataset iterator 优化keras model预测的吞吐量](./tensorflow/replace-placeholder-with-iterator.md)



## 其他

1. [Redis in Action笔记](./Redis/redis-in-action-notes.md)
2. [Mysql cookbook笔记](./Mysql/mysql-cook-book-notes.md)
3. [docker学习笔记1： docker基本使用方法](./Docker/docker-basic-note.md)
4. [xv6 内存管理](./Os/xv6/memory.md)
