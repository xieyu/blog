# Kafka Controller zk监听

在broker当选为controller之后，controller会在zk上注册一堆的handler， 处理broker/topic/partions等变化

```scala
  private def onControllerFailover(): Unit = {
    info("Registering handlers")

    // before reading source of truth from zookeeper, register the listeners to get broker/topic callbacks
    val childChangeHandlers = Seq(brokerChangeHandler, topicChangeHandler, topicDeletionHandler, logDirEventNotificationHandler,
      isrChangeNotificationHandler)
    childChangeHandlers.foreach(zkClient.registerZNodeChildChangeHandler)
    val nodeChangeHandlers = Seq(preferredReplicaElectionHandler, partitionReassignmentHandler)
    nodeChangeHandlers.foreach(zkClient.registerZNodeChangeHandlerAndCheckExistence)
    //...other code
  }
```

## Broker

`BrokerChangeHandler`, 处理broker上线下线

![controller-failover-zk-broker](./controler-failover-zk-broker.svg)

## Topic

### topic change
![topic-change](./topic-change.svg)

### topic delete

![topic-delete](./topic-delete.svg)


## Isrchange

主要更新controller中的cache，并且controller发送sendUpdateMetadata通知所有的borker更新metadata.
![isr-change](./isr-change.svg)

## LogDirEvent

![logdir-event](./logdir-event.svg)


## ReplicaLeaderElection

![replica-leader-election](./controller-process-replica-leader-election.svg)

## PartitionReassignment

![partion-reassignment](./controller-partition-reasignment.svg)
