# Backgroud flush and compaction

## MaybeScheduleFlushOrCompaction

`MaybeScheduleFlushOrCompaction`会使用线程池调度，最后在后台线程中调用`BackgroundFlush`
和`BackgrondCompaction`分别做memtable的flush和ssfile的compaction.

![MaybeScheduleFlushOrCompaction](./MaybeScheduleFlushOrCompaction.svg)


## 后台线程调度Schedule

![schedule-bgtread](./schedule-bgthread.svg)

## 后台线程flush

### 生成flushRequest放入flush队列中

后台线程会去`flush_queue_`队列中去获取要flush的memtable, 向`flush_queue_`中放入FlushRequest流程如下:

![flush_queue_put](./flush_queue_put.svg)

具体细节如下：

![flush queue put detail](./flush_queue_put_detail.svg)


### 后台线程处理flush队列中请求

后台线程执行`BackgroundFlush`从`flush_queue_`中取出FlushRequest转换为FlushJob. 


![flush-data-flow-overview](./flush-data-flow-overview.svg)

cfd会被flush的条件
```cpp
bool MemTableList::IsFlushPending() const {
  if ((flush_requested_ && num_flush_not_started_ > 0) ||
      (num_flush_not_started_ >= min_write_buffer_number_to_merge_)) {
    assert(imm_flush_needed.load(std::memory_order_relaxed));
    return true;
  }
  return false;
}
```

最终调用`WriteLevel0Table` 将memtable写入磁盘中，具体调用关系如下:

![backgroud-flush](./background-flush.svg)

## 后台线程compact

### cfd放入compact队列

![background-compaction-put](./background-compaction-put.svg)


### 处理compact队列，生成compactionJob

后台线程会通过`PickCompactionFromQueue` 去`compaction_queue_`中取出需要compact的ColumnFamilyData,
然后调用ComlumnFamilyData的PickCompaction 选择compactio的input level, output leve, 以及input files等，

![backgroup-compaction](./background-compaction.svg)


#### 多线程并发compact
在compact Prepare中会将compactJob划分为不同的SubCompactionState，然后由多线程并发执行压缩

![background-compaction-job](./background-compaction-job.svg)

#### Compaction Picker

三种compaction style

Level Style Compaction

Universal Style Compaction

FIFO Style Compaction
