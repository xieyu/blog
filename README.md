
建议看[html版本](https://xieyu.github.io/blog/)

# 个人技术博客

## Contents

- [TiDB](#TiDB)
- [TiKv](#TiKv)
- [LevelDB](#LevelDB)
- [RocksDB](#LevelDB)
- [Tensorflow](#Tensorflow)
- [GoRuntime](#Golang)
- [Kafka](#Kafka)

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

- [代码模块间关系](./src/leveldb/code-struct.md)
- [Read 流程](./src/leveldb/read.md)
- [Write 流程](./src/leveldb/write.md)
- [SSTable 文件格式和读写](./src/leveldb/table-format.md)
- [versionset和Manifest文件](./src/leveldb/versionset.md)
- [Compact](./src/leveldb/table-compact.md)
- [Iterator迭代器](./src/leveldb/iterator.md)

### RocksDB

- [主要struct引用关系](./src/rocksdb/column-family.md)
- [Write Ahead Log](./src/rocksdb/wal.md)
- [write 并发控制](./src/rocksdb/write.md)
- [后台flush和compact线程](./src/rocksdb/flush-and-compact.md)
- [Leveled Compaction Picker](./src/rocksdb/leveled-compaction-picker.md)
- [read 流程](./src/rocksdb/read.md)
- [Blob](./src/rocksdb/blob.md)
- [事务](./src/rocksdb/transaction.md)
  - [Optimistic Transaction](./src/rocksdb/optimistic-transaction.md)
  - [Transaction lock mgr](./src/rocksdb/transaction-lock-mgr.md)
  - [two phase commit](./src/rocksdb/two-phase-commit.md)

### TiDB

- [tidb学习资料整理](./src/tidb/note.md)
- [Server Main Loop](./src/tidb/main.md)
- [Insert 语句](./src/tidb/insert.md)
- [Select 语句](./src/tidb/select.md)
- [数据类型](./src/tidb/types.md)
- [expression](./src/tidb/expression.md)
- [Online DDL](./src/tidb/ddl.md)
    - [Schema 存储](./src/tidb/ddl-schema-in-tikv.md)
    - [Schema Cache和加载](./src/tidb/ddl-schema-load.md)
    - [Schema Modification](./src/tidb/ddl-schema-modification.md)
    - [Online Schema Change](./src/tidb/ddl-online-schema-change.md)
- [统计信息](./src/tidb/stat.md)
    - [基本概念](./src/tidb/basic-concepts.md)
    - [stats tables](./src/tidb/stat-tables.md)
    - [Analyze](./src/tidb/stat-analyze.md)
    - [Query Feedback](./src/tidb/stat-feedback.md)
    - [统计信息使用场景](./src/tidb/use-stat.md)
- [Logical Optimize](./src/tidb/logical-optimize.md)
- [Physical Optimize](./src/tidb/physical-optimize.md)
- [DataSource](./src/tidb/datasource.md)
    - [buildDataSource](./src/tidb/datasource-build.md)
    - [索引范围计算](./src/tidb/range.md)
    - [table/index存储编码](./src/tidb/tablecodec.md)
    - [paritionProcessor](./src/tidb/datasource-paritionProcessor.md)
    - [PredicatePushDown](./src/tidb/datasource-predict-push-down.md)
    - [Physical Optimize](./src/tidb/datasource-physical-optimize.md)
    - [Executors](./src/tidb/datasource-executors.md)
- [DistSQL](./src/tidb/distsql.md)
    - [ReginCache](./src/tidb/cop-region-cache.md)
    - [TiKV GRPC Client](./src/tidb/tikv-grpc-client.md)
    - [CopTask](./src/tidb/cop-task.md)
    - [CopIteratorWorker](./src/tidb/cop-iterator-worker.md)
    - [Coprocessor](./src/tidb/coprocessor.md)
- [Join](./src/tidb/join.md)
    - [Join算法](./src/tidb/join-alg.md)
    - [Logical Optimize](./src/tidb/join-logical-optimize.md)
    - [Physical Optimize](./src/tidb/join-physical-optimize.md)
    - [Executor: Hash Join](./src/tidb/hash-join.md)
    - [Executor: Merge Join](./src/tidb/merge-join.md)
    - [Executor: Index Lookup Join](./src/tidb/index-lookup-join.md)
- [Agg](./src/tidb/agg.md)
    - [AggFunc](./src/tidb/agg-func.md)
    - [Executor: HashAgg](./src/tidb/hash-agg.md)
    - [Executor: StreamAgg](./src/tidb/stream-agg.md)

## TiKV
  - [raft-rs](./src/tikv/raft2.md)
    - [RawNode](./src/tikv/raft_rawnode.md)
    - [Storage](./src/tikv/raft_storage.md)
    - [ProgressTracker](./src/tikv/progress_tracker.md)
    - [Hearbeat](./src/tikv/raft_hearbeat.md)
    - [Election](./src/tikv/raft_election.md)
    - [LogEntry](./src/tikv/raft_log_entry.md)
    - [Snapshot](./src/tikv/raft_snapshot.md)
    - [ConfChange](./src/tikv/raft_conf_change.md)
    - [ReadIndex](./src/tikv/raft_read_index.md)
  - [RaftKV](./src/tikv/raft-kv.md)
    - [BatchSystem](./src/tikv/batch-system2.md)
    - [RaftMessage](./src/tikv/raft_message.md)
    - [Raft Client](./src/tikv/raft_client.md)
    - [Region](./src/tikv/region2.md)
    - [PeerStorage](./src/tikv/peer_storage2.md)
    - [Thread Local Engine](./src/tikv/thread_local_engine.md)
    - [Leader Lease](./src/tikv/leader_lease.md)
    - [Read Index](./src/tikv/read_index.md)
    - [Async Snapshot](./src/tikv/async_snapshot2.md)
    - [Async Write](./src/tikv/async_write2.md)
    - [Region Epoch](./src/tikv/region_epoch.md)
    - [Conf Change](./src/tikv/conf_change2.md)
    - [Split Region](./src/tikv/split_region2.md)
    - [Merge Region](./src/tikv/merge_region2.md)
  - [Storage](./src/tikv/storage2.md)
    - [Percolator](./src/tikv/percolator.md)
    - [Percolator In TiKV](./src/tikv/percolator_in_tikv.md)
    - [2PC](./src/tikv/tikv_2pc.md)
    - [AsyncCommit](./src/tikv/async_commit.md)
    - [OnePC](./src/tikv/tikv_1pc.md)
    - [悲观事务](./src/tikv/pessimistic_lock.md)
    - [Resolve Lock](./src/tikv/txn_recovery.md)
    - [Scheduler](./src/tikv/scheduler2.md)
    - [Wait Lock](./src/tikv/wait_lock.md)
    - [死锁检测](./src/tikv/dead_lock.md)
    - [TiDB分组提交](./src/tikv/group_commit.md)
    - [Scanner](./src/tikv/storage_scanner.md)
  - [Coprocessor](./src/tikv/coprocessor.md)
      - [RpnExpression](./src/tikv/rpn_expression.md)
      - [AggrFunction](./src/tikv/aggr_function.md)
      - [BatchExecutor](./src/tikv/batch_executor.md)
        - [RangesScanner](./src/tikv/ranges_scanner.md)
        - [ScanExecutor](./src/tikv/scan_executor.md)
        - [Selection](./src/tikv/batch_executor_selection.md)
        - [AggExecutor](./src/tikv/batch_executor_agg.md)
  - [yatp](./src/tikv/yatp.md)

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
