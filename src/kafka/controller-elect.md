
## Kafka Controller 选举

每个kafka broker启动后, 会去zk中尝试创建ControllerZNode, 如果成功就会当选为controller。然后调用`onControllerFailover`开始controller的工作

 * 从zk中加载数据，刷新controllerContext中的各种cache.
 * 在zk中注册broker, topic, patition等zk处理函数.
 * 启动channelManager, 建立和其他broker之间通信channel
 * 启动PartitionStateMachine和ReplicaStateMachine管理分区和副本状态.
 * 启动kafkaScheduler，启动后台调度等

![controller-elect](./controller-elect.svg)
