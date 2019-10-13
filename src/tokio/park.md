# park

park是对当前线程block和unblock操作的抽象, 和std的park/unpark操作来比，在线程被blocked的时候，可以去调用一些定制化的功能。

## Park impl

![park](./park.svg)

### Reactor Park

Reactor 相关数据结构如下, 
![reactor-park-struct](./reactor-park-struct.svg)


Par接口的park/unpark操作主要依赖于mio的poll和SetReadness。
![reactor-park](./reactor-park.svg)


### Thread pool default park

线程池的default park主要依赖于croess beam的park和unpark

![threadpool_default_park](./threadpool_default_park.svg)

### ParkThread

数据结构之间关系

![park-thread-struct](./park-thread-struct.svg)


接口调用关系

![park-thread](./park-thread.svg)
