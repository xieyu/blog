Tensorflow源码学习
----------

## Core

### Common runtime

* [Executor draft](./tensorflow/executor.md)
* [DirectSession](./tensorflow/direct-session.md)
* [Rendezvous](./tensorflow/rendezvous.md)
* [Device](./tensorflow/device.md)
* Allocator
* ResourceMgr
* Tensor
* OpKernelContext

### OpKernel
* OpKernel
* Variable
* Assign
* MatMul
* Convel


### Distribute Runtime

* GrpcSession
* Master, Worker, MasterSession, WorkerSession
* RDMA
* MPI


## 源码写作技巧总结

* Factory 模式
* impl 模式
* template special 模板特化

UPDATE 
	{{.tablePushStat}} as p,
	(
		SELECT 
			sum(success) as success,
			sum(failure) as failure
		FROM
			{{.tableDelivery}} d
		WHERE d.message_id = message_id
	) as stat
SET
	p.delivery_success +=  {{.incSuccess}},
	p.delivery_failure +=  {{.incFailure}}
WHERE
	p.message_id = {{.messageID}}
`
