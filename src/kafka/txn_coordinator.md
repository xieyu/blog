# Txn coordinator

## FindCoordinator

partition的leader为txn的coordinator

![txn-find-coordinator](./txn-find-coordinator.svg)

## InitProducerId

生成全局唯一producerId, 每个transactionId对应着一个TransactionMetadata,
其中的topicPartitions 该事务涉及到的topic partition set.

![txn-producer-id](./txn-producer-id.svg)


## AddPartitionsToTxn

向事务添加Partitions

![txn-addPartitions](./txn-add-partition.svg)


## endTxn


### PrepareCommit/PrepareAbort

![txn-end](./txn-end.svg)


## Ref

1.[Transactions in Apache Kafka](https://www.confluent.io/blog/transactions-apache-kafka/)
