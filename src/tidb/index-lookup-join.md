# Index Lookup Join

<!-- toc -->

## IndexLookUpJoin Struct

![](./dot/index_lookup_join_struct.svg)

## 主要流程

执行index lookup join时候，会启动一个outerWorker go routine和多个innerWorker go routine, go routine之间通过innerCh和resultCh来协作，
他们关系如下：

* `outerWorker` 负责读取probe side 数据，然后建立map，创建完毕后，将task 同时放入`innerCh`中和`resultCh`中
* `innerWorker` 从innerCh取task，去inner表取数据，执行完毕后，将task的doneCh close用以通知Main线程（执行IndexLookupJoin.Next的groutine)
* 调用IndexLookupJoin.Next的groutine从 resultCh中取一个task, 然后等待task执行完毕，执行完毕后做join, 将数据返回给上层调用者。

![](./dot/index_lookup_join_flow.svg)

### buildTask

buildTask builds a lookUpJoinTask and read outer rows.

When err is not nil, task must not be nil to send the error to the main thread via task.

![](./dot/index_lookup_join_buildtask.svg)

### handleTask


![](./dot/index_lookup_join_handletask.svg)

#### buildExecutorForIndexJoin

![buildExecutorForIndexJoin](./dot/build_executor_for_index_join.svg)

## 参考资料
1. [TiDB 源码阅读系列文章（十一）Index Lookup Join](https://pingcap.com/blog-cn/tidb-source-code-reading-11/)
2. [wikipedia: Nested_loop_join](https://en.wikipedia.org/wiki/Nested_loop_join)
