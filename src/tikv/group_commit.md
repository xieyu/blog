# 分组提交

TiDB 提交事务时，会先将mutation按照key的region做分组，
然 每个分组会分批并发的提交。

doActionOnBatches 这个对primaryBatch的commit操作做了特殊处理。

![](./dot/doActionOnMuations.svg)

### groupMutations: 按照region分组

先对mutations做分组，如果某个region的mutations 太多。
则会先对那个region先做个split, 这样避免对单个region
too much write workload.

![](./dot/tidb_groupmutations.svg)

### doActionOnGroupMutations: 分批

doActionOnGroupMutations 会对每个group的mutations 做进一步的分批处理。
对于actionCommit做了特殊处理，如果是NormalCommit, primay Batch要先提交，
然后其他的batch可以新起一个go routine在后台异步提交。

![](./dot/tidb_doActionOnGroupMutations.svg)

### batchExecutor: 并发的处理batches

`batchExecutor::process` 每个batch会启动一个go routine来并发的处理,
并通过channel等待batch的处理结果。当所有batch处理完了，再返回给调用者。

其中会使用令牌做并发控制, 启动goroutine前先去获取token, goroutine运行
完毕，归还token。

![](./dot/tidb_doActionOnBatches.svg)

## CommitterMutations

数据结构引用关系如下:

![](./dot/commiter_mutations.svg)
