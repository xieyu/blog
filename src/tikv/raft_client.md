# RaftClient

<!-- toc -->


## trait Transport

```rust
/// Transports messages between different Raft peers.
pub trait Transport: Send + Clone {
    fn send(&mut self, msg: RaftMessage) -> Result<()>;

    fn need_flush(&self) -> bool;

    fn flush(&mut self);
}
```

raft client使用方式如下，先send 将消息放入队列中，最后flush，才真正的发送消息。

```rust
/// A raft client that can manages connections correctly.
///
/// A correct usage of raft client is:
///
/// ```text
/// for m in msgs {
///     if !raft_client.send(m) {
///         // handle error.   
///     }
/// }
/// raft_client.flush();
/// ```
```

## ServerTransport


![](./dot/server_transport.svg)

### connection pool

![](./dot/raft_client_connection_pool.svg)

### connection builder

![](./dot/raft_client_connection_builder.svg)




### RaftClient的创建

![](./dot/raft_client_new.svg)


## 主要函数调用流程

### send

先从LRUCache 中获取`(store_id, conn_id)`对应的Queue，如果成功, 
则向 Queue中push raftMessage, 如果push消息时返回Full错误，就调用`notify`，
通知RaftCall 去`pop` Queue消息, 将消息发送出去。

如果`LRUCache`中没有，则向Connection Pool中获取，如果获取还失败的话，则创建一个。

![](./dot/raft_client_send1.svg)

最后在future pool中执行`start`, 

### `load_stream`

![](./dot/raft_client_load_stream.svg)

### start

start会异步的调用`PdStoreAddrResolver`去resolve `store_id`的addr, 
然后创建连接。

调用`batch_call` 新建一个`RaftCall`. 
`RaftCall`被poll时会不断的去Queue中pop 消息, 并通过grpc stream将消息发出去。


由于包含snap的Message太大，会有`send_snapshot_sock`专门处理


![](./dot/raft_client_start.svg)

### resolve: store addr解析

在`TiKVServer::init`时，store addr resolve worker，会在background yatp 线程池中执行。
调用者使用`PdStoreAddrResolver`来向add resolver线程
发消息。它创建流程如下:

![](./dot/create_resolver.svg)

Resolve流程如下：addr-resolver worker收到消息后，先本地cache中看查看有没有store 的addr，如果没有或者
已经过期了，就调用PdClient的`get_store`方法，获取store的addr地址。

成功后回调`task_cb`函数，在该回调函数中会触发`oneshot_channel`, StreamBackEnd::resolve 接着执行
await resolve后边代码。

![](./dot/raft_client_resolve.svg)

### snapshot 发送和接收

#### `send_snap`

包含snap的RaftMessage消息体比较大，将由`snap-handler` worker来发送.

snap-handler的worker创建和启动流程如下：

![](./dot/create_snap_handler.svg)

`send_snapshot_sock` 使用`scheduler`的tx，向`snap-handler`
worker 发送`SnapTask::Send` Task, snap-handler worker 调用`send_snap`创建
发送snap的异步任务，然后在上面创建的Tokio 线程池Runtime中执行。

`send_snap`会去snap manager获取snapshot 构造一个SnapChunk
然后创建和peer所在store addr的grpc connection channel，使用`snapshot`grpc调用
将SnapChunk数据发送给peer.

SnapChunk实现了Stream trait, 在`poll_next`中调用`read_exact`一块块的将snap数据发出去。

![](./dot/send_snap.svg)


#### `recv_snap`

![](./dot/recv_snap.svg)

### `broadcast_unreachable`

往`store_id`消息失败, 向自己所有region广播store unreachable消息


![](./dot/raft_client_broadcast_unreachable.svg)


### 参考

1. [Snapshot 的发送和接收](https://pingcap.com/blog-cn/tikv-source-code-reading-10)

## draft

![](./dot/raft_client_draft.svg)

![](./dot/raft_client_send.svg)

![](./dot/raft_client_send_snap_sock.svg)


