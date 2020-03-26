# 个人技术博客

## 读书笔记

### Design Data Intensive Application
- [Consistency And Consensus](./src/ddia/consistency-and-consensus.md)
- [Transactions](./src/ddia/transactions.md)

### Specifying System

- [基本定义概念整理](./src/specifying-systems/basic-concepts.md)


## 代码阅读笔记
### Golang

- [Runtime PGM调度模型](./src/golang/pgm.md)
- [Goroutine stack](./src/golang/goroutine-stack.md)
- [Go 内存分配](./src/golang/memory.md)
- [GC](./src/golang/GC.md)
- [Context](./src/golang/context.md)
- [defer, panic, recover](./src/golang/defer-panic-recover.md)

### Kafka

- [log日志存储管理](./src/kafka/log.md)
- [Partition](./src/kafka/partition.md)
- [Controller 主要功能](./src/kafka/controller-main.md)
- [Controller 通信管理 channelManager](./src/kafka/controller-channel-manager.md)
- [Controller 选举](./src/kafka/controller-elect.md)
- [Controller zk监听](./src/kafka/controller-zk.md)
- [Controller 副本迁移](./src/kafka/replica-assignment.md)
- [Partition/Replica状态机](./src/kafka/paritition-replica-statemachine.md)
- [读写消息](./src/kafka/kafka-produce-fetch.md)
- [client: producer](./src/kafka/client-producer.md)
- [group coordinator](./src/kafka/group-coordinator.md)
- [事务](./src/kafka/txn_coordinator.md)
- [Stream流处理](./src/kafka/stream.md)

### LevelDB

- [Read 流程](./src/leveldb/read.md)
- [Write 流程](./src/leveldb/write.md)
- [SSTable 文件格式和读写](./src/leveldb/table-format.md)
- [versionset和Manifest文件](./src/leveldb/versionset.md)

### TiDB

- [TiDB Server Main Loop](./src/tidb/main.md)
- [TiDB Plan](./src/tidb/plan.md)
- [TiDB Hasjoin draft](./src/tidb/hash-join.md)


### Tokio

- [Executor: 执行future](./src/tokio/executor.md) ``Executor``主要作用是spawn future，将future转换为相应的task，然后由runtime去执行task，不断的调用future的poll接口, 直到future complete 或者fail。
  - [Park 线程block/unblock抽象](./src/tokio/park.md) Park是对当前线程block和unblock操作的抽象, 和std的park/unpark操作来比，在线程被blocked的时候，可以去调用一些定制化的功能。
  - [thread pool runtime](./src/tokio/thread-pool.md) tokio 使用了crossbeam中的Queue, Stealer, Worker等来实现线程池。采用work steal机制来保证任务均匀分配。
- [Driver: mio事件驱动](./src/tokio/driver.md) Driver 在io event事件触发后，唤醒等待的task。
- [Io: async read/write 等抽象](./src/tokio/io.md)

### Tensorflow

- [Executor: 执行Computation Sub Graph](./src/tensorflow/executor.md)
    - [SubGraph预处理：Node/NodeItem/TaggedNode](./src/tensorflow/executor-subgraph-preprocess.md)
    - [Flow control op: switch/merge/enter/exit/nextIteration](./src/tensorflow/flow-control-op.md)
    - [Frame: ControlFlowInfo/FrameInfo/FrameState/IterationState](./src/tensorflow/executor-frame.md)
- [DirectSession: 单机执行computation graph](./src/tensorflow/direct-session.md)
- [RendezVous：跨设备，跨主机通信](./src/tensorflow/rendezvous.md)
- [Device：计算单元抽象(CPU/GPU)](./src/tensorflow/device.md)
