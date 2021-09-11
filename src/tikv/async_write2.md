# Async Write

<!-- toc -->

## 提交raft proposal

Peer调用raft RawNode::propose方法，将RaftCmdRequest 提交给raft log, 
然后将write callback和要写入的log entry的index放入了本地的proposals等待队列。

这个地方和ReadIndex一样，会带上当前时间戳，作为后续renew lease的时间戳

![](./dot/peer_propose_normal.svg)


## 处理raft committed

leader节点在应用propse log entry后，会将该log entry先保存在本地，然后复制到各个follower上，待集群中大部分节点
都保存了该log entry时， log entry达到comitted 状态，TiKV可以安全的把它apply 到kv engine上了。

Peer在`handle_raft_committed_entries`时，会根据log entry的term和index找到它在proposals队列中
对应的proposal, 然后主要做如下工作

1. renew leader lease, 使用proposal时候的时间戳来更新leader lease.
2. 调用该proposal cb的`invoke_comitted`。
3. 将comitted entries和它们的cbs 打包发给apply fsm处理。

![](./dot/peer_handle_raft_committed.svg)



## Apply to KvEngine

comitted entries, 连同它对应的Proposals， 被路由到ApplyFsm后，由ApplyFsm 负责执行comitted entries中的`RaftCmdRequest`
保存完毕后，调用回调`cb.invoke_with_response`,通知write 已经apply 到kv engine了.

这些Proposals首先会被放到`ApplyDelegate::pending_cmds`队列中, 等raft cmd被执行完毕后，
从`ApplyDelegate::pending_cmds`队列中，找到对应的Proposal, 然后将它的callback 放入
`ApplyContext::cbs`中。

最后再`ApplyContext::flush`时, 回调`ApplyContext::cbs`中的callback, 然后将ApplyRes 发
给PeerFsm.

![](./dot/applyfsm_handle_apply.svg)


### RaftApplyState

处理完一个comitted entry后，会更新`applied_index_term`和`applied_index`
这两项会放到ApplyRes，后面通知PeerFsm, PeerFsm会更新PeerStorage中的
`apply_state`和`applied_index_term`.

在生成snaptask时，也会用到这两项。

![](./dot/apply_RaftApplyState.svg)

### exec raft cmd

write有四种命令，`Put`, `Delete`, `DeleteRange`, `IngestSst`, 其中put/delete是写到write batch上的。

![](./dot/ApplyDelegate__exec_write_cmd.svg)


### ApplyResult::yield

每次`ApplyPoller::handle_normal`时，会在`ApplyDelegate::handle_start`中记录开始的时间，
然后在`ApplyDelegate::handle_raft_entry_normal`, 每次处理一个raft log entries,
如果需要write batch需要写入kv engine的话，就调用ApplyContext::commit，将write batch
提交，然后计算已经消耗的时间。如果时间超过`ApplyContext::yield_duration`, 就返回ApplyResult::yield.

在`ApplyDelegate::handle_raft_committed_entries`中，会将剩余的committed entries 保存到
`ApplyDelegate::yield_state`中。

等下次重新开始`handle_normal`时，先调用`resume_pending`, 先处理`ApplyDelegate::yield_state`中的log 
entries.

![](./dot/ApplyResult__yield.svg)
