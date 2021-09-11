# TiDB 事务

> * TiDB在Pecolator基础上增加了并发Prewrite, AsyncCommit和OnePC提交，实现了悲观事务。
> * TiDB的Mutations(key的put/delete)会先保存在MemDB中, 在2PC中分region, 分批, 并发的提交这些修改。
> * TiKV返回RegionError时，TiDB要重新按照region 做分组，分批，然后重新提交。
> * TiKV在lock冲突时，会等待一段时间或者等key release了, 再返回client，key conflict或者deadlock错误。避免client无效的重试。

<!-- toc -->
## 数据流程

TiDB中乐观事务提交流程如下(摘自[TiDB 新特性漫谈：悲观事务][6]):

![](./dot/Optimistic_pecolator.png)

1. 首先Begin 操作会去TSO服务获取一个timestamp，作为事务的`startTS`.
2. DML阶段先KVTxn将写(Set, Delete)操作保存在MemDB中。
3. 悲观事务会在DML 阶段去TiKV获取悲观lock。
4. 2PC提交阶段 在`KVTxn::Commit`时创建`twoPhaseCommitter`, 并调用它的`initKeysAndMutations`
遍历`MemDB`, 初始化`memBufferMutations`.

在`twoPhaseCommitter::execute`中，首先对`memBufferMutations`先按照region做分组，
然后每个分组内，按照size limit分批。最后每批mutations,调用对应的action
的`handleSignleBatch`，发送相应命令到TiKV.

![](./dot/batch_mutation.svg)










## 参考文献

[TiDB 悲观锁实现原理](https://asktug.com/t/topic/33550)
2. [async commit design spec](https://github.com/tikv/sig-transaction/blob/master/design/async-commit/spec.md)
3. [async commit and replica read](https://tikv.github.io/sig-transaction/design/async-commit/replica-read.html)
4. [support checking memory locks at read index](https://github.com/pingcap/kvproto/pull/665)

[1]: https://asktug.com/t/topic/33550
[async-commit]: https://pingcap.com/blog-cn/async-commit-principle/
[3]: https://book.tidb.io/session1/chapter6/pessimistic-txn.html
[6]: https://pingcap.com/blog-cn/pessimistic-transaction-the-new-features-of-tidb/


# draft


### KeyFlags

### MemDB



## Questions:

1. 如果某个prewrite batch失败了，其他正在执行，或者已经执行的Prewrite batch是怎么rollback的？
2. async commit, one pc commit, minCommitTS, PessimisticLock 这几单独拿出来专题研究。
3. 同一个事物只能在同一个TiDB上跑吗？
4. ForUpdateTS 这个是干什么用的？

```rust
        // The isolation level of pessimistic transactions is RC. `for_update_ts` is
        // the commit_ts of the data this transaction read. If exists a commit version
        // whose commit timestamp is larger than current `for_update_ts`, the
        // transaction should retry to get the latest data.
```

![](./dot/tidb_txn.svg)

## Timestamp

### commitTS

事务提交的commitTs, 在commit之前去time oracle 服务获取timestamp.

### MinCommitTs/MaxCommitTs

>线性一致性实际上有两方面的要求：

>循序性（sequential）

>实时性（real-time）

>实时性要求在事务提交成功后，事务的修改立刻就能被新事务读取到。新事务的快照时间戳是向 PD 上的 TSO 获取的，这要求 Commit TS 不能太大，最大不能超过 TSO 分配的最大时间戳 + 1。

async commit会用到minCommitTs, 省去了一次去Time服务获取tso的操作。

每个TiKV server有个ConcurrencyManager 记录了max_ts

> 对于 Async Commit 事务的每一个 key，prewrite 时会计算并在 TiKV 记录这个 key 的 Min Commit TS，事务所有 keys 的 Min Commit TS 的最大值即为这个事务的 Commit TS。
> TiDB 的每一次快照读都会更新 TiKV 上的 Max TS。Prewrite 时，Min Commit TS 会被要求至少比当前的 Max TS 大2，也就是比所有先前的快照读的时间戳大，所以可以取 Max TS + 1 作为 Min Commit TS。


```rust
	// If we want to use async commit or 1PC and also want linearizability across
	// all nodes, we have to make sure the commit TS of this transaction is greater
	// than the snapshot TS of all existent readers. So we get a new timestamp
	// from PD and plus one as our MinCommitTS.
	if commitTSMayBeCalculated && c.needLinearizability() {
		failpoint.Inject("getMinCommitTSFromTSO", nil)
		latestTS, err := c.store.oracle.GetTimestamp(ctx, &oracle.Option{TxnScope: oracle.GlobalTxnScope})
		// If we fail to get a timestamp from PD, we just propagate the failure
		// instead of falling back to the normal 2PC because a normal 2PC will
		// also be likely to fail due to the same timestamp issue.
		if err != nil {
			return errors.Trace(err)
		}
		// Plus 1 to avoid producing the same commit TS with previously committed transactions
		c.minCommitTS = latestTS + 1
	}

	// Calculate maxCommitTS if necessary
	if commitTSMayBeCalculated {
		if err = c.calculateMaxCommitTS(ctx); err != nil {
			return errors.Trace(err)
		}
	}
```

maxCommitTs的作用是什么？

Tikv 在async_commit_timestamps 中会检查min_commit_ts和max_commit_ts
如果min_commit_ts > max_commit_ts 会返回CommitTsTooLarge

![](./dot/tidb_min_commit_ts.svg)



### onePCCommitTS

## cleanup

事务回滚？

![](./dot/tidb_txn_cleanup.svg)

finishStmt

## SimpleExec

![](./dot/SimpleExec.svg)
### 获取悲观锁: LockKeys

![](./dot/tidb_pessimisticlock.svg)

KeyFlags

```go
	flagPresumeKNE KeyFlags = 1 << iota
	flagKeyLocked
	flagNeedLocked
	flagKeyLockedValExist
	flagNeedCheckExists
	flagPrewriteOnly
	flagIgnoredIn2PC
	persistentFlags = flagKeyLocked | flagKeyLockedValExist
```

