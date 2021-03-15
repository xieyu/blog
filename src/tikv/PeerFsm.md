# PeerFsm

<!-- toc -->

## raft-rs

TiKV调用RawNode的地方

![](./dot/tikv-call-raft-rs.svg)

### tick

![](./dot/tikv-rawnode-tick.svg)

谁在发送PeerMsg Tick呢？

![](./dot/tikv-schedule-tick.svg)

### ready

![](./dot/tikv-rawnode-ready.svg)

谁触发了ready 呢？

write batch是在什么时候apply的？为什么？

### 处理`Apply<EK::Snapshot>`

![](./dot/ApplyFsm.svg)

### handle raft log

![](./dot/raftlog.svg)

handle_raft_ready里面

```
        if !ready.entries().is_empty() {
            self.append(&mut ctx, ready.take_entries(), ready_ctx)?;
        }
```

### 处理 `ApplyRes<Ek::Shapshot>`

![](./dot/handle-apply-res.svg)

### advance_append

![](./dot/tikv-rawnode-advance-append.svg)

谁发送了`PeerMsg::ApplyRes` ?

### step

从kv grpc接口发送的消息，最后发送到了RawNode_step

![](./dot/tikv-rawnode-step.svg)

### propose

![](./dot/tikv-rawnode-proposal.svg)


### readIndex

kv get

![](./dot/tikv-kv-get.svg)

LocalReader_read

![](./dot/local_reader_read.svg)

propose read index

![](./dot/tikv-rawnode-read-indx.svg)

apply reads

![](./dot/tikv-apply-reads.svg)

### LeaseRead

#### PeerMsg::RaftCommand

![](./dot/tikv-RaftCommand.svg)

## kv Service


![](./dot/tikv-service.svg)

[TiKV 源码解析系列文章（十一）Storage - 事务控制层](https://pingcap.com/blog-cn/tikv-source-code-reading-11/)

### ServerRaftStoreRouter



## RocksEngine

![](./dot/RocksEngine.svg)


### RocksSnapshot

### RocksWriteBatch


### RaftLogBatch

## Node

## RaftLog

