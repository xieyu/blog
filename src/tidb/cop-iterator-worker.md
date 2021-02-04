# CopIteratorWorker

Coprocessor 中通过copIteratorWorker来并发的向tikv(可能是多个tikv sever) 发送请求.

Worker负责发送RPC请求到Tikv server，处理错误，然后将正确的结果放入respCh channel中
在copIterator Next方法中会respCh中获取结果。

![dist sql](./dot/dist_sql.svg)
