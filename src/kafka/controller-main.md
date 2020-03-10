# Kafka Controller 主要功能

kafka中会从broker server中选取一个作为controller，该controller通过ControllerChannelManager管理和每个broker通信的线程。

当zk中broker,topic, partion 等发生变动时，controller向每个broker发送消息, replica和partition 主要是通过replicaStateMachine和PartitionStateMachine来管理的
当replica或者partition leaderAndISR信息发生变动时候，controller通过这两个状态机，将状态的转换改为
相应的request请求，发送给broker。 

其中比较重要的请求是LeaderAndISR, 它指定了partition的leader和paritition in sync的replica list。

每个broker在zk中注册了ControllerChangeHandler，如果controller挂了，broker就会尝试去选举新的controller.


![allpartionsoverview](./allpartion-overview.svg)


controller会向broker发送三类请求: 

* UpdateMetadataRequest: 更新元数据
* LeaderAndIsrRequest: 创建分区，副本，leader和follower
* StopReplicaRequest: 停止副本。

controller和broker之间同步metadata

三类请求broker主要处理逻辑如下：

![broker_update_metadata](./broker_update_metadata.svg)

controller和broker之间处理IsrAndLeader请求

![borker-handle-isr](./broker_handle_isr.svg)

controller向broker发送stopReplica请求

![broker-stop-relica](./broker-stop-replica.svg)


