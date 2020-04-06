# Draft


## Class之间关系

![class-relations](./class-relations.svg)


## Write

1. 最终怎么写到了memTable中。
2. WAL写的流程是什么样？

![write](./write.svg)

## WriteBatch

![write-batch](./write-batch.svg)

## ColumnFamily

1. Blob 中value和key是怎么对的上的？
2. 数据结构之间怎么串起来的。 

column family 相关数据结构之间引用关系

![column_family](./column_family.svg)

## Write Thread

Writer的状态
![write thread state](./write_thread_state.svg)

write thread过程
Write group leader 负责写入WAL日志。
memtable可能由group leader写，也有可能由各个writer 并发写。

write thread是对写线程的抽象
![write thread](./write_thread.svg)

write 相关struct之间引用关系

![write struct](./write_struct.svg)


write impl
![pipelined-write impl](./pipline_writeimpl.svg)


## 后台压缩

MaybeScheduleFlushOrCompaction

![flush-compaction](./flush_compaction.svg)

后台线程调度Schedule

![schedule-bgtread](./schedule-bgthread.svg)

后台刷新mem到磁盘上

![backgroup-flush](./background-flush.svg)

后台线程压缩

![backgroup-compaction](./background-compaction.svg)
