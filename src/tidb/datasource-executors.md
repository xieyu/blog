# Executors

<!-- toc -->

## TableReaderExecutor

PhyscialTableReader对应的Executor为TableReaderExecutor, 其build过程如下:

![build physical table reader](./dot/build_physical_table_reader_executor.svg)

TableReaderExecutor 对应的Open/Next/Close调用，其中对TiKV层的调用封装在了distsql模块中。

![table reader executor](./dot/table_reader_executor.svg)


## TableIndexExecutor

PhysicalIndexReader 对应的Execturo为TableIndexExecutor, 其build过程如下:

![build_index_reader](./dot/build_index_reader.svg)

IndexExecutor Open/Next/Close方法, 也调用了distsql的方法

![table_index_reader_exexutor](./dot/table_index_reader_executor.svg)

## IndexLookUpExecutor

PhysicalIndexLookUpReader 对应的Execturo为IndexLookupReader, 其build过程如下:

![build_index_lookup_executor](./dot/build_index_lookup_executor.svg)

index Worker/Table Worker

![IndexLookUpExecutor](./dot/IndexLookUpExecutor.svg)


### extractTaskHandles

从index中获取row handlers

![](./dot/extractTaskHandlers.svg)

### buildTableReader

根据row handlers 去获取相应的Row

![](./dot/buildTableReader.svg)

## DistSQL

上面的TableReaderExecutor/TableIndexExecutor/IndexLookUpExecutor 最后 
都会去调用DistSQL模块的代码, 去TiKV请求数据。
