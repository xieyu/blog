# 后台刷盘和压缩过程

## MaybeScheduleFlushOrCompaction

触发后台刷盘和压缩过程

![MaybeScheduleFlushOrCompaction](./MaybeScheduleFlushOrCompaction.svg)

## 后台线程池Schedule

### 后台线程调度Schedule

![schedule-bgtread](./schedule-bgthread.svg)

### 后台刷盘过程

`BackgrounFlush`最终通过WriteLevel0Table将memtable写入disk中

![backgroup-flush](./background-flush.svg)

### 后台压缩过程

TODO: compaction job的数据来源需要梳理一下

![backgroup-compaction](./background-compaction.svg)
