# 事务Recovery

Pecolator的coordinator在完成commit或者rollback之前crash了，
事务遗留的Lock，由后续事务的在处理lock冲突时，resolve lock.
将事务的lock提交了或者rollback。

写冲突时候，先检查lock的ttl，如果lock已经查超时了, 则会调用`getTxnStatus`，获取事务状态。


NormalCommit可以根据Primay key状态来确定整个事务的状态和commitTs(commitTs=0，表示
loc需要被rollback)

AsyncCommit则需要扫描所有的keys来确定事务的状态和minCommitTS.
如果所有的Key的lock都exsit，那么事务的commitTs 应该为所有key lock
的minCommitTS的最大值。


### resolveLocksForWrite

先调用`getTxnStatus`获取primary lock状态，然后和当前write事务冲突的secondary key做`commit`或者`rollback`.

![](./dot/resolveLocksForWrite.svg)


### resolveLockAsync

在`addKeys`中，会根据lock的minCommitTS，更新事务的commitTS.
如果lock个数比key的个数少，说明有的key的lock已经被commit或者rollback了,
则会用返回的commitTS作为事务的commitTS 
(如果被rollback了，TiKV返回的CommitTs为0).


![](./dot/tidb_async_commit_recovery.svg)

```go
// addKeys adds the keys from locks to data, keeping other fields up to date. startTS and commitTS are for the
// transaction being resolved.
//
// In the async commit protocol when checking locks, we send a list of keys to check and get back a list of locks. There
// will be a lock for every key which is locked. If there are fewer locks than keys, then a lock is missing because it
// has been committed, rolled back, or was never locked.
//
// In this function, locks is the list of locks, and expected is the number of keys. asyncResolveData.missingLock will be
// set to true if the lengths don't match. If the lengths do match, then the locks are added to asyncResolveData.locks
// and will need to be resolved by the caller.
func (data *asyncResolveData) addKeys(locks []*kvrpcpb.LockInfo, expected int, startTS uint64, commitTS uint64) error {
  //...
	// Check locks to see if any have been committed or rolled back.
	if len(locks) < expected {
		// A lock is missing - the transaction must either have been rolled back or committed.
		if !data.missingLock {
			// commitTS == 0 => lock has been rolled back.
			if commitTS != 0 && commitTS < data.commitTs {
				return errors.Errorf("commit TS must be greater or equal to min commit TS: commit ts: %v, min commit ts: %v", commitTS, data.commitTs)
			}
			data.commitTs = commitTS
		}
		data.missingLock = true

		if data.commitTs != commitTS {
			return errors.Errorf("commit TS mismatch in async commit recovery: %v and %v", data.commitTs, commitTS)
		}
    //...
```



![](./dot/resolveLocksForWriteAsyncCommit.svg)

### resolveRegionLocks
 resolveRegionLocks is essentially the same as resolveLock, but we resolve all keys in the same region at the same time.

![](./dot/resolve_region_locks.svg)



