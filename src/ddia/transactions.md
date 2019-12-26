# Transactions

### Transactions

a Transaction in a way for an application to group server reads and write together into a logical unit.
Conceptlly, all the reads and writes in the transactions are execute as one operations, either the entire 
transaction succeeds(commit) or it fails(abort, rollback), app can safely retry.

事物作为一个整体要么成功(commit)，要么失败(abort/rollback), 失败的事务应用可以安全的重试。

### ACID

#### Atomic (原子性)

ACID atomicity describes what happens if a client wants to make serveral writes, but a fault occurs after some of the writes have been
processed(for example a process crashed, network connection is interrupted). if the writes are grouped together into an atomic transaction,
the transaction is aborted and the database must discard or undo any writes it has made so far in transaction;

失败的事务可以回滚，不会影响数据库，不会出现部分成功，部分失败的场景，应用可以安全的重试，


#### Consistency (一致性)

In the context of ACID, consistency referes to an application specific notion of the database being in a good state.

数据库中的数据保持良好的状态，比如银行账号转账能保持balance.


#### Isolation (隔离性)

Isolation in the sense of ACID means that concurrently excuting transactions are isolated from each other.

the database ensures thath when the transactions have commited, the result is the same as if they had run 
serally.

隔离性：并发的事务之间执行互相之间没影响, 就像顺序执行的那样。由于严格的Serializable的Isolation　性能代价比较高，因此有各种稍微弱(weak)一些的隔离等级。
比如: read commited, snapshot isolation, Serializability.


#### Durability (持久化)

Durability is the promise that once a transaction has commited successfully, and data it has written will no be forgooten, even if there is a hardware fault
or the database crashes

事务成功提交后，它的数据不会丢失，即使database crash了，或者发生了硬件故障。 主要有两种手段WAL(write ahead log)和replica(副本)


## Weak Isolation Levels

### Read commited

the most basic level of transaction isolation is read committed. It makes two guarantees:

1. When reading from database, you will only see data that has been committed. (no dirty reads)
2. when writing to database, you will only overwrite data that has been commited (no dirty writes)

未提交的事务, 所写的数据在数据库中不可见，既不会被读到，也不会其它事务的写所覆盖.


实现方式：

1.使用row-level lock

database prevent dirty writes by using row-level locks. when a transaction wants to modify a particular object, it must
first acquire a lock on that object. It must then hold that lock util the transaction is commited or aborted

2. mvcc 使用多版本
the database remembers both the old committed value and the new vlaue set by the transaction that current holds the write lock.;

### Snapshot Isolation and Repeatable Read

#### Read skew(nonrepeatable read)

在转账过程中，短暂的不一致问题, 无法容忍短暂不一致的场景

1. Backup

数据库备份,如果数据库备份时候，数据库正好不一致，那么所备份的数据就不一致了。

2. Analytic quries and integrity checks
