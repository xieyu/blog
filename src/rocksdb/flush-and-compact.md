# 后台刷盘和压缩过程

### MaybeScheduleFlushOrCompaction

`MaybeScheduleFlushOrCompaction`会使用线程池调度，最后在后台线程中调用`BackgroundFlush`
和`BackgrondCompaction`分别做memtable的flush和ssfile的compaction.

![MaybeScheduleFlushOrCompaction](./MaybeScheduleFlushOrCompaction.svg)


### 后台线程调度Schedule

![schedule-bgtread](./schedule-bgthread.svg)

### 后台线程flush


后台线程会去`flush_queue_`队列中去获取要flush的memtable, 向`flush_queue_`中放入FlushRequest流程如下:

![flush_queue_put](./flush_queue_put.svg)

具体细节如下：
![flush queue put detail](./flush_queue_put_detail.svg)

后台线程从`flush_queue_`中取出FlushRequest转换为FlushJob. 

![flush-data-flow-overview](./flush-data-flow-overview.svg)

最终调用`WriteLevel0Table` 将memtable写入磁盘中，具体调用关系如下:

![backgroud-flush](./background-flush.svg)

### 后台线程compact

TODO: compaction job的数据来源需要梳理一下

![backgroup-compaction](./background-compaction.svg)

#### Compaction Picker

三种compaction style

Level Style Compaction

Universal Style Compaction

FIFO Style Compaction
