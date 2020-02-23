# Kafka 读写消息


## 消息的produce and consume

![kafka-produce-fetch](./kafkaServer.svg)


## partition 对应log对象创建

log对象是什么时候创建的？parition创建时候就创建吗？

![kafka-log-create](./partition-log-create.svg)


## ReplicaManager Partion信息维护

ReplicaManager的allPartions是存放在zk中的吗？不同broker server之间这个信息是怎么同步的?

当zk中broker,topic, partion, controller等发生变动时候，由kafka controller通过ControllerChannelManager
向每个kafka broker发送``LEADER_AND_ISR``消息, broker收到消息以后，会更新ReplicaManager中的allPartitions信息。

![allpartionsoverview](./allpartion-overview.svg)


具体细节如下
![getPartition](./getpartition.svg)

