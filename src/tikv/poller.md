# Poller

<!-- toc -->

## poll

![](./dot/poller_poll.svg)


## RaftPoller

![](./dot/raft-poller.svg)

### PeerFsmDelegate::handle_msgs

最终会调用Raft-rs模块的RawNode.propose

![](./dot/tikv-rawnode-proposal.svg)

## ApplyPoller
