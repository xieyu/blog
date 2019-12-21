# Consistency and Consensus(一致性和共识)

本文对design data intensive application中的chapter 9中的内容做了一些摘抄，以及备注了一些自己的理解


## Consistency Guarantees (一致性保证)

### eventual consistency(最终一致性)

the inconsistency is temporary, and it eventually resolve itself;

a better name for eventual consistency may be convergence, as we expect all replicas to eventually convergence to the same value;

数据库副本之前由于存在延迟，所以某些时刻，副本之间会存在短暂的不一致的情况，但是过一段时间(多长时间没保证)会收敛到相同值。

由于多长时间没保证，该一致性保证比较弱。app可能在此期间读不同的副本，读到不一致的值，从而导致各种bug...


### linearizability(线性一致性)

make a system appear as if there were only one copy of the data and all operations on it are atomic;

最强的一致性保证, 和Total Order BroadCast之间的关系还需要再研究下。

### CAP

Consistency, Availability, Partition tolerance

when a network fault occurs, you have to choose between either linearizability or total availability;

当发生网络故障的时候，线性一致性和完全可用两者只能选一个.

## Order Guarantees

some context in which we have discussed ordering:

1. single leader replication: the purpose of leader in single leader replication is to determinate the order or writes;
2. serializability: ensure that transaction behave as if they were execute in some sequnetial oerder
3. time stamps and clock: in distributed systems attempt to introduce order to a disorderly world

### Causality(因果关系)

Causality impose an ordering on events: cause comesed before effect. the chain of causally dependent operations define the causal order in the system
what happened before what.

因果关系定义了事件的先后关系，因果关系链决定了一系列事件的先后关系。在因果关系链上的事务和操作需要前后串行执行，没在因果关系链上的操作可以并发的执行。

### Total Order(全序)

total order allows any two elements to be compared, in linearizability system we have a total order of operations, for any two operations we can always
say which one happened first

### Partially order(偏序)

in some cases one is greater than other, but in other cases they are incomparable

we say that two operations are concurrent if neither happened before another, two events are ordered if they are causally related(one happened before another);

causally defines a partial order, but not total order:

### Lamport timestamps

lamport timestamp is then simply a pair of (counter, nodeID)

every node and every clients keep track of maxium counter value it has seen so far, and include that maximum on every request

when a node recive a maximum counter value greater than it's owner counter, it immediately increase it's own counter to maximum;

为什么这这种方式可以作为逻辑时钟？还没理解的很透彻

光有lamport timestaps是不够的，书上举了unique user name的例子，还需要再看看。

### Total Order BroadCast

total order broad cast describe as a protocol for exchange messages between nodes, requires:

1. **Reliable delivery**: no message are lost, if message is delivery to one node, it is delivered to all nodes;
2. **Total Order Delivery**: messages are delivered to every node in the **same** order;

require message to be delivered exactly once, in the same order, to all nodes;

Total Order BroadCast  linearizability 这两者之间是啥关系？

此处没怎么看明白，需要接着研究。

### Two phase commit (两阶段提交)

分为prepare 和 commit 阶段，需要有一个coordinate.

coordinate sends a prepare request to each of the nodes, asking them whether they are able to commit;

1. if all paritcipants reply "yes", indicating they are ready commit, then the coordinate send out a commit request in phase 2 and the commit actully take place.
2. if nay of the paritcipants replies "no", the coordinate sends an abort request to all nodes in phase 2;

key points:

1. coordinate generate a unique transaction ID
2. when paritcipants reply "yes", it make sure that it can definitely commit the transaction under all circumstances
3. commit point: when coordinate has recived reponse to all prepare requests, the coordinate must write the descision to it's transaction log on disk
4. once the coordinate descision write tot disk, coordinate make sure it can definitely finish the descision; coordinate retry forever util it succeds;

我觉得两阶段提交关键点在于

只要参与者reply了yes, 那么它可以保证自己无论在什么情况下，都能完成commit, 
只要coordinate 做了决定(abort or commit)，就一定能保证各个节点都能收到commit/abort。

