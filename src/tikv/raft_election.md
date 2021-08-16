# Election

### PreCandidate

在follower成为candidate之前，会先成为PreCandidate
然后发起prevote投票，prevote请求并<b>不会增大term</b>
如果赢得了prevote选举，才会变为Candidate，发起真正的选举.

### tick election: 发起投票

发起election

![](./dot/tick-election.svg)

### handle MsgRequestVote/MsgRequestPreVote

主要会检查m.term(消息的term)和自己term, 以及candidate的日志是否足够新

```rust
MessageType::MsgRequestVote | MessageType::MsgRequestPreVote => {
    // We can vote if this is a repeat of a vote we've already cast...
    let can_vote = (self.vote == m.from) ||
        // ...we haven't voted and we don't think there's a leader yet in this term...
        (self.vote == INVALID_ID && self.leader_id == INVALID_ID) ||
        // ...or this is a PreVote for a future term...
        (m.get_msg_type() == MessageType::MsgRequestPreVote && m.term > self.term);
    // ...and we believe the candidate is up to date.
    if can_vote
        && self.raft_log.is_up_to_date(m.index, m.log_term)
        && (m.index > self.raft_log.last_index() || self.priority <= m.priority)
    {
     //发送prove Resp
     }else {
     //发送reject resp
     }
```

### handle MsgRequestPreVoteResponse/MsgRequestVoteResponse

![](./dot/handle_msg_vote_resp.svg)
