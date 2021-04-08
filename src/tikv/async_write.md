# async write

<!-- toc -->

## RaftKV::async_write

发送消息给raftStore,并等待回调。

txn的modifies 转换为RaftCmdRequest， 发往RaftStore
然后RaftStore在处理该消息调用回调.

![](./dot/raftkv_async_write.svg)

## RaftRouter::send_command

//TODO


## PeerFsmDelegate::handle_msgs

![](./dot/PeerFsmDelegate_handle_RaftCmdRequest.svg)


## PeerFsmDelegate::collect_ready


![](./dot/PeerFsmDelegate_collect_ready_write.svg)


## ApplyFsm::handle_tasks

![](./dot/ApplyPoller_handle_normal.svg)
