# RocksDB Write流程

## WriteBatch

![write-batch](./write-batch.svg)

## PreprocessWrite

### schedule flush

schedule flush, 将满的memtable转变为immtable, 加到`flush_schedule_`队列中
由`BackgrounFlush`将immtable刷到dish上。

![schedule flush](./schedule_flushes.svg)


## Write thread

Writer的状态

![write thread state](./write_thread_state.svg)

write 相关struct之间引用关系

![write struct](./write_struct.svg)
