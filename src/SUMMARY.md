# Summary
- [About](./about.md)
- [tensorflow inside](./tensorflow/index.md)
  - [Executor: 执行Computation Sub Graph](./tensorflow/executor.md)
      - [SubGraph预处理：Node/NodeItem/TaggedNode](./tensorflow/executor-subgraph-preprocess.md)
      - [Flow control op: switch/merge/enter/exit/nextIteration](./tensorflow/flow-control-op.md)
      - [Frame: ControlFlowInfo/FrameInfo/FrameState/IterationState](./tensorflow/executor-frame.md)
  - [DirectSession: 单机执行computation graph](./tensorflow/direct-session.md)
  - [RendezVous：跨设备，跨主机通信](./tensorflow/rendezvous.md)
  - [Device：计算单元抽象(CPU/GPU)](./tensorflow/device.md)

- [tensorflow model optimize](./tensorflow/optimize.md)
  - [将keras模型导出为tf frozen graph](./tensorflow/export-keras-model-as-tf-frozen-graph.md)
  - [使用dataset iterator 优化keras model预测的吞吐量](./tensorflow/replace-placeholder-with-iterator.md)
  - [统计cpu/gpu 负载率脚本](./tensorflow/stat-cpu-gpu-load.md)

- [pthread](./pthread/index.md)
  - [Pthread Primer笔记](./pthread/pthread-primer.md)
  - [Pthread线程生命周期](./pthread/glibc-pthread-implement-thread-life-cycle.md)
  - [Pthread线程同步](./pthread/glibc-pthread-implement-sync.md)

- [react](./react/index.md)
    - [从jsx到html dom的流程分析](./react/from-jsx-to-dom.md)

- [hotspot](./java/index.md)
  - [osx下编译调试hotspot](./java/hotspot-debug-under-osx.md)
  - [jvm的初始化时创建的线程](./java/hotspot-thread-created-when-init.md)
  - [class文件的加载和执行](./java/hotspot-class-file-load-and-run.md)
