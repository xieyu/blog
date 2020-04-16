# OptimisticTransaction


![optimistic transaction](./optimistic-transaction.svg)

![check key conflict](./check-key-conflict.svg)

一些问题：

1. 根据什么判断是否有冲突的？貌似是根据sequnceNumber，但是具体细节不太清楚
2. `bucketed_locks_`的作用是啥？
3. CommitWithSerialValidate和 CommitWithParallelValidate这两者区别是啥？

![optimistic transaction commit](./optimistic-transaction-commit.svg)
