# park

Abstraction over blocking and unblocking the current thread.

Provides an abstraction over blocking the current thread. This is similar to
the park / unpark constructs provided by [`std`] but made generic. This
allows embedding custom functionality to perform when the thread is blocked.

## Park impl

![park](./park.svg)

### Reactor Park

![reactor-park](./reactor-park.svg)

### Thread pool default park

![threadpool_default_park](./threadpool_default_park.svg)

### ParkThread

![park-thread](./park-thread.svg)
