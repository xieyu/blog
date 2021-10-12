# OnePC(一阶段提交)


![](./dot/one-pc.png)

只涉及一个region，且一个batch就能完成的事务，不使用分布式提交协议，只使用一阶段完成事务，
和AsyncCommit相比， 省掉了后面的commit步骤。


![](./dot/twoPhaseCommitter_one_pc_execute.svg)

对于batchCount > 1的事务不会使用OnePC.

```go
func (c *twoPhaseCommitter) checkOnePCFallBack(action twoPhaseCommitAction, batchCount int) {
	if _, ok := action.(actionPrewrite); ok {
		if batchCount > 1 {
			c.setOnePC(false)
		}
	}
}
```

#### Tikv端 处理OnePC

在TiKV端，OnePC 直接向Write Column 写write record, 提交事务，
省掉了写lock, 以及后续commit时候cleanup lock这些操作了。

![](./dot/tikv_one_pc.svg)

