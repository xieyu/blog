# Hearbeat


## leader: `send_heartbeat`

leader定时向所有成员发送Heartbeat, 注意，这块的commit 是`min(pr.matched, self.raft_log.committed)`

```rust
// Attach the commit as min(to.matched, self.raft_log.committed).
// When the leader sends out heartbeat message,
// the receiver(follower) might not be matched with the leader
// or it might not have all the committed entries.
// The leader MUST NOT forward the follower's commit to
// an unmatched index.
```

![](./dot/leader_heartbeat.svg)

### follower/candidate: `handle_heartbeat`

如果从leader收到的msg term >= self.term,
会重置heartbeat_timeout时间，然后更新raft_log的committed_index

![](./dot/follower_handle_heartbeat.svg)

### leader: `handle_heartbeat_response`

![](./dot/handle_heartbeat_response.svg)
