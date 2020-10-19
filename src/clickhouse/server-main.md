# Server Main 

<!-- toc -->

## Server main 主流程

### 主循环

首先监听端口号，等待客户端连接， 
和客户端建立连接后,server然后不断从conn中读取packet, 
解析sql语句为AST树，然后创建plan pipeline
最后执行plan，将result set通过网络发送给客户端.

![server-main](./dot/server-main.svg)


### SQL 解析执行流程

一条Query SQL在clickhouse中执行流程如下:

![execute-flow](./dot/execute-flow.svg)

#### Parse SQL

解析SQL，解析为AST树，然后创建对应的pipeline plan.

![execute-query](./dot/execute-query.svg)

#### SelectQuery  

执行Select Query , 创建QueryPlan

![select-query](./dot/select-query.svg)

#### QueryPlanStep

![query-plan-step](./dot/query-plan-step.svg)

#### IProcessor 

 Processor is an element (low level building block) of a query execution pipeline.
It has zero or more input ports and zero or more output ports.

Blocks of data are transferred over ports.
Each port has fixed structure: names and types of columns and values of constants.

```
src/Processors/IProcessor.h
```

#### IProcessor 继承关系图

CK中Iprocessor的继承关系图

```cpp
class IProcessor
{
protected:
    InputPorts inputs;
    OutputPorts outputs;
}
```
![iprocessor](./dot/iprocessor.svg)

![transform](./dot/transform.svg)

### Executor: 执行pipeline

#### PipelineExecutor

使用线程池执行pipline

![pipeline-executor](./dot/pipeline-executor.svg)


#### PullingPipelineExecutor

单线程同步执行？

```cpp
/// Pulling executor for QueryPipeline. Always execute pipeline in single thread.
/// Typical usage is:
///
/// PullingPipelineExecutor executor(query_pipeline);
/// while (executor.pull(chunk))
///     ... process chunk ...
```

![pulling-pipeline-executor](./dot/pulling-pipeline-executor.svg)

#### PullingAsyncPipelineExecutor

多线程异步执行


```cpp
/// Asynchronous pulling executor for QueryPipeline.
/// Always creates extra thread. If query is executed in single thread, use PullingPipelineExecutor.
/// Typical usage is:
///
/// PullingAsyncPipelineExecutor executor(query_pipeline);
/// while (executor.pull(chunk, timeout))
///     ... process chunk ...
```

![pulling-async-pipeline-executor](./dot/pulling-async-pipeline-executor.svg)

### IBlockInputStream

#### PipelineExecutingBlockInputStream

封装了PullingPipelineExecutor和PullingAsyncPipelineExecutor, 实现了IBlockInputStream接口

![pipeline-executing-block-input-stream](./dot/pipeline-executing-block-input-stream.svg)

#### AsynchronousBlockInputStream


在另外一个线程中执行inner BlockInputStream
```cpp
/** Executes another BlockInputStream in a separate thread.
  * This serves two purposes:
  * 1. Allows you to make the different stages of the query execution pipeline work in parallel.
  * 2. Allows you not to wait until the data is ready, and periodically check their readiness without blocking.
  *    This is necessary, for example, so that during the waiting period you can check if a packet
  *     has come over the network with a request to interrupt the execution of the query.
  *    It also allows you to execute multiple queries at the same time.
  */
```

![asynchronous-block-inputstream](./dot/asynchronous-block-inputstream.svg)

### BlockIO
block-io getInputStream，读数据时执行plan

![block-io](./dot/block-io.svg)

## 参考资料

1. [Clickhouse源码导读: 网络IO](https://cloud.tencent.com/developer/article/1602664)
2. [Clickhouse源码导读](http://sineyuan.github.io/post/clickhouse-source-guide/)
3. [ClickHouse 源码阅读 —— SQL的前世今生](https://developer.aliyun.com/article/765184)
