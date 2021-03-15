

### start_system

![](./dot/RaftBatchSystem_start_system.svg)


## poller

### poll
![](./dot/poller_poll.svg)
![](./dot/tikv-peerfsm-datastruct.svg)

![](./dot/tikv-fsm.svg)

谁在向poller的fsm_receiver中发消息呢？

这部分在上面的create_raft_batch_system已经搞定了。

猜测router负责使用tx发送消息,system 从rx中接收消息，然后处理消息。

![](./dot/poller-fsm-receiver.svg)

![](./dot/tikv-poll.svg)
