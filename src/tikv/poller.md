# Poller

<!-- toc -->

## poll

![](./dot/poller_poll.svg)


## RaftPoller

![](./dot/raft-poller.svg)

### StoreFsmDelegate::handle_msgs

### PeerFsmDelegate::handle_msgs

消息最后都会调用`raft-rs`的RawNode相关方法.

![](./dot/PeerFsmDelegate_handle_msgs.svg)

### PeerFsmDelegate::collect_ready

将日志写入raft_wb, snapshot写入kv_wb中(只写入了write_batch，还没落盘)。

使用apply router, 通知ApplyPoller 处理committed raftlog日志。

![](./dot/PeerFsmDelegate_collect_ready.svg)

### RaftPoller::handle_raft_ready

调用`Transport.flush` 发送raft 消息，将raft_wb, kv_wb写入rocksdb中。
使用apply router, 通知ApplyPoller 处理committed raftlog日志。

![](./dot/RaftPoller_handle_raft_ready.svg)

### PeerFsmDelegate::on_apply_res

主要调用raft-rs的advance_apply，还有处理read_index

![](./dot/PeerFsmDelegate_on_apply_res.svg)


## ApplyPoller

![](./dot/ApplyPoller.svg)

### AppDelegate::handle_raft_committed_entries

![](./dot/AppDelegate_handle_raft_normal.svg)


### ApplyPoller::end

![](./dot/ApplyPoller_end.svg)
