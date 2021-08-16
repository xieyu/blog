# LogEntry

### propose

app 希望向 Raft 系统提交一个写入时，需要在 Leader 上调用 RawNode::propose 方法

![](./dot/RawNode_propose.svg)

### follower: handle_append_entries

![](./dot/follower_handle_append_entries.svg)

### leader: handle_append_response

progressMap

leader 处理follower的append entries 的回复。
在哪里判断收到了大部分follower的确认?
怎么更新自己的commit index的?

![](./dot/handle_append_response.svg)
