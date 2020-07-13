# Server Main 

<!-- toc -->

## Server main 主流程

### 主循环

首先监听端口号，等待客户端连接， 
和客户端建立连接后,server然后不断从conn中读取packet, 
解析sql语句为AST树，然后创建plan pipeline
最后执行plan，将result set通过网络发送给客户端.

![server-main](./dot/server-main.svg)


### SQL 执行流程

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

#### PipelineExecutor

使用线程池执行pipline

![pipeline-executor](./dot/pipeline-executor.svg)

block-io getInputStream，读数据时执行plan
![block-io](./dot/block-io.svg)

## Ref

[Clickhouse源码导读: 网络IO](https://cloud.tencent.com/developer/article/1602664)
