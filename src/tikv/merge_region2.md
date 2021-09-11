# Region Merge

<!-- toc -->

Merge Region时，PD先将source region和targer Region 的TiKV节点对齐。

## Merge流程

理解的关键点

1. Source region 在向target region 提交CommitMerge前,怎么发现和处理target region发生了变动
2. source region的`on_catch_up_logs_for_merge`和`on_ready_prepare_merge`这两个被调用时序问题。
3. target和source region之间通过CatchUpLogs中的atomic `catch_up_logs`,来同步补齐的状态。

## 相关RaftCmdRequest

在merge region中，主要涉及到的raft cmd为PrePareMergeRequest和CommitMergeRequest

PrepareMergeRequest 将由source region来proposal并执行，在source region执行PrepareMerge时，
PeerState为Merging, 并在RaftLocalState中保存了一个`MergeState`。然后发CommitMergeRequest给本地的`target region`, 

target region把CommitMergeRequest proposal到target region的raft group后，
由target region来执行CommitMerge.

![](./dot/RegionMergeProto.svg)

## PrepareMerge

### Source Region: propose PrepareMerge

Source Region leader在leader收到PrepareMerge请求后，会propose 一条PrepareMerge消息。

propose 之前会做一些检查, 最后会设置PrePareMerge中的`min_index`参数

![](./dot/prepare_merge.svg)

在ApplyFsm执行PrepareMerge时，region的epoch和`conf_version`都会+1,
这样PrepareMerge 之后Proposal的log entry 在Apply时都会被skip掉。
所以soure region在propose PreapreMerge 之后，就不可读写了。


### Source Region `ApplyDelegate::exec_prepare_merge`

将PeerState设置为Merging, 将region epoch的`conf_ver`和version 都+1

![](./dot/exec_prepare_merge.svg)


### Source Region `PeerFsmDelegate::on_ready_prepare_merge`

![](./dot/PeerFsmDelegate__on_ready_prepare_merge.svg)

source region raft 在收到ExecResult::PreapreMerge消息之后， 会调用`on_ready_prepare_merge` 处理该消息。
首先设置了`pending_merge_state`，在此之后，该region raft 对于proposal(RollbackMerge的除外)请求，会返回Error::ProposalInMergeMode.

```rust
    fn propose_normal<T>(
        &mut self,
        poll_ctx: &mut PollContext<EK, ER, T>,
        mut req: RaftCmdRequest,
    ) -> Result<Either<u64, u64>> {
        if self.pending_merge_state.is_some()
            && req.get_admin_request().get_cmd_type() != AdminCmdType::RollbackMerge
        {
            return Err(Error::ProposalInMergingMode(self.region_id));
        }
```

然调用`on_check_merge`, 经过一系列检查后， 向本地的target region Propose 一条CommitMergeRequest消息,
CommitMergeRequest 带上了source region一些peer要补齐的log entries.

其中比较重要的方法是`Peer::validate_merge_peer`, 会检查Source的MergeState 中的target region信息
和当前本地target region信息。如果merge state中的比本地的epoch小，则返回错误。

如果比本地的大，则需要等target region epoch 追上后再`schedule_merge`,
在下一次check merge tick中接着检查。



向本地target region发送AdminCmdType::CommitMerge类型的RaftCmd.

```rust
// Please note that, here assumes that the unit of network isolation is store rather than
// peer. So a quorum stores of source region should also be the quorum stores of target
// region. Otherwise we need to enable proposal forwarding.
self.ctx
    .router
    .force_send(
        target_id,
        PeerMsg::RaftCommand(RaftCommand::new(request, Callback::None)),
    )
    .map_err(|_| Error::RegionNotFound(target_id))
```

处理Schedule Error: RegionNotFound, 以及target region epoch比merge state中的大。

![](./dot/PeerFsmDelegate__schedule_merge_error.svg)


## RollbackMerge

RollbackMerge执行后，会将`pending_merge_state`设置为none, 这样
就停止了`on_check_merge`, 并且`propose_normal`也可以正常工作了

RollbackMerge会将region epoch的version +1, 然后通过pd hearbeat
上报给pd server.

![](./dot/source_region_rollback_merge.svg)

## CommitMerge

### Target Region `ApplyDelegate::exec_commit_merge`

CommitMerge消息由source region 发给本地的target region后，如果本地
的target region是leader， 则会像正常消息一样propose 到raft group,
如果target region不是leader, 则会slient drop掉该消息。

在target节点执行CommitMerge时，会先发送一个CatchUpLogs消息，给本地的source region
让它把日志补齐，CatchUpLogs里面带了一个`logs_up_to_date`是个AtomicU64.

如果source region补齐了log, 则会设置`logs_up_to_date`为自己的`region_id`。

`ApplyDelegate::wait_merge_state` 也引用了`logs_up_to_date`，每次`resume_pending`
都会load `logs_up_to_date`，如果有值，则会继续重新执行`exec_commit_merge`.

将target region的key range扩大, 增加target region的version, 最后调用
`write_peer_state`将target region信息保存起来。

![](./dot/ApplyDelegate__exec_commit_merge.svg)

等SourceRegion 已经CatchUpLogs后, 会修改atomic `logs_up_to_date`
从而影响`ApplyDelegate::wait_merge_state`, 在`resume_pending`
时重新执行`exec_commit_merge`。

![](./dot/AppDelegate__exec_commit_merge2.svg)

### Source Region: `PeerFsmDelegate::on_catch_up_logs_for_merge`

使用CommitMergeRequest中的entries，补齐apply自己本地raft log.
，然后发送LogsUpToDate消息个ApplyFsm。

为什么这个地方补齐log就行啦？而不用等到这些log都被apply 到state machine上？
还是说LogsUpToDate消息被ApplyFsm执行前，这些被补齐的Log一定会被执行？
这个地方只有当`pending_merge_state`不为空的时候，也就是PrepareMerge被apply后，才会调到
所以这个地方图要拆成两张来画。

ApplyFsm中设置atomic 变量`CatchUpLogs::logs_up_to_date`值为
`source_region_id`, 然后发Noop消息给target region.

让target region接着处理自己的`wait_merge_state`

![](./dot/catchup_logs.svg)


### Target region: `PeerFsmDelegate::on_ready_commit_merge`

target region的PeerFsm 中更新StoreMeta中regions, readers， `region_ranges`信息，
删除`source_region`的，更新target region的

然后发送SignificantMsg::MergeResult消息给`source_region`.

![](./dot/PeerFsmDelegate__on_ready_commit_merge.svg)



### Source Region: `PeerFsmDelegate::on_merge_result`

destory source regon PeerFsm和ApplyFsm.

如果ApplyFsm还没被注销的话，发送ApplyTask::destory 先destory ApplyFsm.

![](./dot/PeerFsmDelegate__on_merge_result.svg)
