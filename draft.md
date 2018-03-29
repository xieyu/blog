Tensorflow源码学习
----------

## Core

### Common runtime

* [Executor](./tensorflow/executor.md)
* [DirectSession](./tensorflow/direct-session.md)
* [Rendezvous](./tensorflow/rendezvous.md)
* Device
* Allocator
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
