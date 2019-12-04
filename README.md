## 个人技术博客 [ghpage](https://xieyu.github.io/blog/)

### TiDB

- [TiDB Server Main Loop](./src/tidb/main.md)


### Tokio code 阅读系列

- [Executor: 执行future](./src/tokio/executor.md) ``Executor``主要作用是spawn future，将future转换为相应的task，然后由runtime去执行task，不断的调用future的poll接口, 直到future complete 或者fail。
  - [Park 线程block/unblock抽象](./src/tokio/park.md) Park是对当前线程block和unblock操作的抽象, 和std的park/unpark操作来比，在线程被blocked的时候，可以去调用一些定制化的功能。
  - [thread pool runtime](./src/tokio/thread-pool.md) tokio 使用了crossbeam中的Queue, Stealer, Worker等来实现线程池。采用work steal机制来保证任务均匀分配。
- [Driver: mio事件驱动](./src/tokio/driver.md) Driver 在io event事件触发后，唤醒等待的task。
- [Io: async read/write 等抽象](./src/tokio/io.md)
