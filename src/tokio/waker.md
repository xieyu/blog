# task waker

![task-waker](./task-waker.svg)

## atomic waker

`AtomicWaker` is a multi-consumer, single-producer transfer cell. The cell
stores a `Waker` value produced by calls to `register` and many threads can
race to take the waker by calling `wake`.

Because of this, the task will do one of two things.

1) Observe the application state change that Thread B is waking on. In
   this case, it is OK for Thread B's wake to be lost.

2) Call register before attempting to observe the application state. Since
   Thread A still holds the `wake` lock, the call to `register` will result
   in the task waking itself and get scheduled again.


![atomic-waker-state](./atomic-waker-state.svg)
