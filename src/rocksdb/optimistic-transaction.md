# Optimistic Transaction

## Questions

1. key冲突检测是咋搞的
2. 并行和顺序这个是怎么弄的

乐观事务在commit前，Write操作只会记录事务有哪些key, 不需要做加锁和key冲突检测，适合事务之间
write key重叠比较低的场景。

在commit时候进行key的冲突检测。

![optimistic transaction](./optimistic-transaction.svg)


key冲突检测

![check key conflict](./check-key-conflict.svg)

一些问题：

1. 根据什么判断是否有冲突的？貌似是根据sequnceNumber，但是具体细节不太清楚
2. `bucketed_locks_`的作用是啥？
3. CommitWithSerialValidate和 CommitWithParallelValidate这两者区别是啥？

![optimistic transaction commit](./optimistic-transaction-commit.svg)
