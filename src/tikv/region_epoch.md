# Region Epoch

Region Epoch变更规则如下：

> 1. 配置变更的时候， `conf_ver`+ 1。
> 2. Split 的时候，原 region 与新 region 的 version均等于原 region 的 version+ 新 region 个数。
> 3. Merge 的时候，两个 region 的 version均等于这两个 region 的 version最大值 + 1。

在raft peer之间发送RaftMessage(比如hearbeat, append等消息）时，`Peer::send_raft_message`
会把region的epoch放到RaftMessage中, 然后再发出去.

在raft peer收到消息时，`PeerFsmDelegate::check_msg`中会检查Region Epoch，如果不匹配的话，会drop skip掉这个消息。

在处理上层应用通过raft router发来的RaftCmdRequest时，也会检查它的region epoch和term, 如果不Match会返回EpochNotMatch.

在ApplyFsm 执行raft cmd时，也会检查region epoch，如果不match的话，会返回EpochNotMatch，

![](./dot/region_epoch.svg)

`check_region_epoch`检查逻辑如下

1. 对于normal request，只会检查version.
2. 对于AdminCmd 有个map

```rust
pub struct AdminCmdEpochState {
    pub check_ver: bool,
    pub check_conf_ver: bool,
    pub change_ver: bool,
    pub change_conf_ver: bool,
}


lazy_static! {
    /// WARNING: the existing settings in `ADMIN_CMD_EPOCH_MAP` **MUST NOT** be changed!!!
    /// Changing any admin cmd's `AdminCmdEpochState` or the epoch-change behavior during applying
    /// will break upgrade compatibility and correctness dependency of `CmdEpochChecker`.
    /// Please remember it is very difficult to fix the issues arising from not following this rule.
    ///
    /// If you really want to change an admin cmd behavior, please add a new admin cmd and **do not**
    /// delete the old one.
    pub static ref ADMIN_CMD_EPOCH_MAP: HashMap<AdminCmdType, AdminCmdEpochState> = [
        (AdminCmdType::InvalidAdmin, AdminCmdEpochState::new(false, false, false, false)),
        (AdminCmdType::CompactLog, AdminCmdEpochState::new(false, false, false, false)),
        (AdminCmdType::ComputeHash, AdminCmdEpochState::new(false, false, false, false)),
        (AdminCmdType::VerifyHash, AdminCmdEpochState::new(false, false, false, false)),
        // Change peer
        (AdminCmdType::ChangePeer, AdminCmdEpochState::new(false, true, false, true)),
        (AdminCmdType::ChangePeerV2, AdminCmdEpochState::new(false, true, false, true)),
        // Split
        (AdminCmdType::Split, AdminCmdEpochState::new(true, true, true, false)),
        (AdminCmdType::BatchSplit, AdminCmdEpochState::new(true, true, true, false)),
        // Merge
        (AdminCmdType::PrepareMerge, AdminCmdEpochState::new(true, true, true, true)),
        (AdminCmdType::CommitMerge, AdminCmdEpochState::new(true, true, true, false)),
        (AdminCmdType::RollbackMerge, AdminCmdEpochState::new(true, true, true, false)),
        // Transfer leader
        (AdminCmdType::TransferLeader, AdminCmdEpochState::new(true, true, false, false)),
    ].iter().copied().collect();
}
```

会修改region epoch的RaftAdminCmd
