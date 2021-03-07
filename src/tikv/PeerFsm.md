# PeerFsm

<!-- toc -->

## Data struct

![](./dot/tikv-peerfsm-datastruct.svg)

## RaftPoller


TiKV调用RawNode的地方

![](./dot/tikv-call-raft-rs.svg)

### tick

![](./dot/tikv-rawnode-tick.svg)

谁在发送PeerMsg Tick呢？

![](./dot/tikv-schedule-tick.svg)

### ready

![](./dot/tikv-rawnode-ready.svg)

谁触发了ready 呢？

### advance_append

![](./dot/tikv-rawnode-advance-append.svg)

谁发送了`PeerMsg::ApplyRes` ?

### step

从kv grpc接口发送的消息，最后发送到了RawNode_step

![](./dot/tikv-rawnode-step.svg)

### proposal

![](./dot/tikv-rawnode-proposal.svg)

## poller

谁在向poller的fsm_receiver中发消息呢？

猜测router负责使用tx发送消息,system 从rx中接收消息，然后处理消息。

![](./dot/poller-fsm-receiver.svg)

![](./dot/tikv-poll.svg)

## RaftBatchSystem

## mailBox
