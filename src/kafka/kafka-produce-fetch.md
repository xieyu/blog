# Kafka 读写消息


## 消息的produce and consume

![kafka-produce-fetch](./kafkaServer.svg)


## partition 对应log对象创建

log对象是什么时候创建的？parition创建时候就创建吗？

![kafka-log-create](./partition-log-create.svg)


## ReplicaManager Partion信息维护

ReplicaManager的allPartions是存放在zk中的吗？不同broker server之间这个信息是怎么同步的?
![getPartition](./getpartition.svg)
