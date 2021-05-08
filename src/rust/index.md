# rust

## books futures explained


https://cfsamson.github.io/books-futures-explained/0_background_information.html

### OS Thread, Green Threads, Callback based, Async task


Green threads use the same mechanism as an OS - creating a thread for each task, setting up a stack, saving the CPU's state, and jumping from one task(thread) to another by doing a "context switch".


async, await, Future, Pin


GreenThread 有点像GO的做法.

GreenThread做法

1. Run some non-blocking code.
2. Make a blocking call to some external resource.
3. CPU "jumps" to the "main" thread which schedules a different thread to run and "jumps" to that stack.
4. Run some non-blocking code on the new thread until a new blocking call or the task is finished.
5. CPU "jumps" back to the "main" thread, schedules a new thread which is ready to make progress, and "jumps" to that thread.

GreenThread DrawBacks

1. The stacks might need to grow. Solving this is not easy and will have a cost.
2. You need to save the CPU state on every switch.
3. It's not a zero cost abstraction (Rust had green threads early on and this was one of the reasons they were removed).
4. Complicated to implement correctly if you want to support many different platforms.

去看下GO是怎么解决 1/2的

这个代码可以要仔细研究下
https://cfsamson.gitbook.io/green-threads-explained-in-200-lines-of-rust/

```rust
#![feature(llvm_asm, naked_functions)]
use std::ptr;

const DEFAULT_STACK_SIZE: usize = 1024 * 1024 * 2;
const MAX_THREADS: usize = 4;
static mut RUNTIME: usize = 0;

pub struct Runtime {
    threads: Vec<Thread>,
    current: usize,
}

#[derive(PartialEq, Eq, Debug)]
enum State {
    Available,
    Running,
    Ready,
}

struct Thread {
    id: usize,
    stack: Vec<u8>,
    ctx: ThreadContext,
    state: State,
    task: Option<Box<dyn Fn()>>,
}

#[derive(Debug, Default)]
#[repr(C)]
struct ThreadContext {
    rsp: u64,
    r15: u64,
    r14: u64,
    r13: u64,
    r12: u64,
    rbx: u64,
    rbp: u64,
    thread_ptr: u64,
}

impl Thread {
    fn new(id: usize) -> Self {
        Thread {
            id,
            stack: vec![0_u8; DEFAULT_STACK_SIZE],
            ctx: ThreadContext::default(),
            state: State::Available,
            task: None,
        }
    }
}

impl Runtime {
    pub fn new() -> Self {
        let base_thread = Thread {
            id: 0,
            stack: vec![0_u8; DEFAULT_STACK_SIZE],
            ctx: ThreadContext::default(),
            state: State::Running,
            task: None,
        };

        let mut threads = vec![base_thread];
        threads[0].ctx.thread_ptr = &threads[0] as *const Thread as u64;
        let mut available_threads: Vec<Thread> = (1..MAX_THREADS).map(|i| Thread::new(i)).collect();
        threads.append(&mut available_threads);

        Runtime {
            threads,
            current: 0,
        }
    }

    pub fn init(&self) {
        unsafe {
            let r_ptr: *const Runtime = self;
            RUNTIME = r_ptr as usize;
        }
    }

    pub fn run(&mut self) -> ! {
        while self.t_yield() {}
        std::process::exit(0);
    }

    fn t_return(&mut self) {
        if self.current != 0 {
            self.threads[self.current].state = State::Available;
            self.t_yield();
        }
    }

    fn t_yield(&mut self) -> bool {
        let mut pos = self.current;
        while self.threads[pos].state != State::Ready {
            pos += 1;
            if pos == self.threads.len() {
                pos = 0;
            }
            if pos == self.current {
                return false;
            }
        }

        if self.threads[self.current].state != State::Available {
            self.threads[self.current].state = State::Ready;
        }

        self.threads[pos].state = State::Running;
        let old_pos = self.current;
        self.current = pos;

        unsafe {
           let old: *mut ThreadContext = &mut self.threads[old_pos].ctx;
           let new: *const ThreadContext = &self.threads[pos].ctx;
           llvm_asm!(
               "mov $0, %rdi
                mov $1, %rsi"::"r"(old), "r"(new)
           );
           switch();
       }
        true
    }

    pub fn spawn<F: Fn() + 'static>(f: F){
        unsafe {
            let rt_ptr = RUNTIME as *mut Runtime;
            let available = (*rt_ptr)
                .threads
                .iter_mut()
                .find(|t| t.state == State::Available)
                .expect("no available thread.");

            let size = available.stack.len();
            let s_ptr = available.stack.as_mut_ptr().offset(size as isize);
            let s_ptr = (s_ptr as usize & !15) as *mut u8;
            available.task = Some(Box::new(f));
            available.ctx.thread_ptr = available as *const Thread as u64;
            //ptr::write(s_ptr.offset((size - 8) as isize) as *mut u64, guard as u64);
            std::ptr::write(s_ptr.offset(-16) as *mut u64, guard as u64);
            std::ptr::write(s_ptr.offset(-24) as *mut u64, skip as u64);
            std::ptr::write(s_ptr.offset(-32) as *mut u64, call as u64);
            available.ctx.rsp = s_ptr.offset(-32) as u64;
            available.state = State::Ready;
        }
    }
}

fn call(thread: u64) {
    let thread = unsafe { &*(thread as *const Thread) };
    if let Some(f) = &thread.task {
        f();
    }
}

#[naked]
fn skip() { }

fn guard() {
    unsafe {
        let rt_ptr = RUNTIME as *mut Runtime;
        let rt = &mut *rt_ptr;
        println!("THREAD {} FINISHED.", rt.threads[rt.current].id);
        rt.t_return();
    };
}

pub fn yield_thread() {
    unsafe {
        let rt_ptr = RUNTIME as *mut Runtime;
        (*rt_ptr).t_yield();
    };
}

#[naked]
#[inline(never)]
unsafe fn switch() {
    llvm_asm!("
       mov     %rsp, 0x00(%rdi)
       mov     %r15, 0x08(%rdi)
       mov     %r14, 0x10(%rdi)
       mov     %r13, 0x18(%rdi)
       mov     %r12, 0x20(%rdi)
       mov     %rbx, 0x28(%rdi)
       mov     %rbp, 0x30(%rdi)

       mov     0x00(%rsi), %rsp
       mov     0x08(%rsi), %r15
       mov     0x10(%rsi), %r14
       mov     0x18(%rsi), %r13
       mov     0x20(%rsi), %r12
       mov     0x28(%rsi), %rbx
       mov     0x30(%rsi), %rbp
       mov     0x38(%rsi), %rdi
       "
   );
}
#[cfg(not(windows))]
fn main() {
    let mut runtime = Runtime::new();
    runtime.init();
    Runtime::spawn(|| {
        println!("I haven't implemented a timer in this example.");
        yield_thread();
        println!("Finally, notice how the tasks are executed concurrently.");
    });
    Runtime::spawn(|| {
        println!("But we can still nest tasks...");
        Runtime::spawn(|| {
            println!("...like this!");
        })
    });
    runtime.run();
}
```


promises return a state machine which can be in one of three states: pending, fulfilled or rejected

promise三个状态: pending, fulfilled, rejected

```javascript
function timer(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

timer(200)
.then(() => timer(100))
.then(() => timer(50))
.then(() => console.log("I'm the last one"));
```

```
async function run() {
    await timer(200);
    await timer(100);
    await timer(50);
    console.log("I'm the last one");
}
```

Since promises are re-written as state machines, they also enable an even better syntax which allows us to write our last example like this:

state machines? 为什么 promise可以被rewrite为state machines?



## Futures

A future is a representation of some operation which will complete in the future.

Async in Rust uses a Poll based approach, in which an asynchronous task will have three phases.

1. The Poll phase. A Future is polled which results in the task progressing until a point where it can no longer make progress. We often refer to the part of the runtime which polls a Future as an executor.
2. The Wait phase. An event source, most often referred to as a reactor, registers that a Future is waiting for an event to happen and makes sure that it will wake the Future when that event is ready.
3. The Wake phase. The event happens and the Future is woken up. It's now up to the executor which polled the Future in step 1 to schedule the future to be polled again and make further progress until it completes or reaches a new point where it can't make further progress and the cycle repeats.

### leaf future, non-leaf future

```rust
let mut stream = tokio::net::TcpStream::connect("127.0.0.1:3000");
``

Operations on these resources, like a Read on a socket, will be non-blocking and return a future which we call a leaf future since it's the future which we're actually waiting on.

### non-leaf future

Non-leaf-futures are the kind of futures we as users of a runtime write ourselves using the async keyword to create a task which can be run on the executor.

```rust
let non_leaf = async {
    let mut stream = TcpStream::connect("127.0.0.1:3000").await.unwrap();// <- yield
    println!("connected!");
    let result = stream.write(b"hello world\n").await; // <- yield
    println!("message sent!");
    ...
};
```

The key to these tasks is that they're able to yield control to the runtime's scheduler and then resume execution again where it left off at a later point.

yield 地方下次poll时候，会接着执行。 这个是怎么实现的？有点像thread context switch时候保存stack ptr,下次来的时候，接着执行了。

不知道rust是怎么实现的? state每次  async 对应的task结构是？
switch(state) {
case state1:
  xxx code
  yield: set state to state2
case state2:
  xxx code
}

In contrast to leaf futures, these kind of futures do not themselves represent an I/O resource. 
When we poll them they will run until they get to a leaf-future which returns Pending and then yield control to the scheduler (which is a part of what we call the runtime).


Mental Model

A fully working async system in Rust can be divided into three parts:

Reactor
Executor
Future

Reactor 表示最底层事件？

So, how does these three parts work together? 
They do that through an object called the Waker.
The Waker is how the reactor tells the executor that a specific Future is ready to run.
Once you understand the life cycle and ownership of a Waker, you'll understand how futures work from a user's perspective.
Here is the life cycle:

A Waker is created by the executor. 
A common, but not required, method is to create a new Waker for each Future that is registered with the executor.

When a future is registered with an executor, 
it’s given a clone of the Waker object created by the executor.
Since this is a shared object (e.g. an Arc<T>), all clones actually point to the same underlying object.
Thus, anything that calls any clone of the original Waker will wake the particular Future that was registered to it.

The future clones the Waker and passes it to the reactor, which stores it to use later.


Rust 标准库关注的：接口..

What Rust's standard library takes care of

1. A common interface representing an operation which will be completed in the future through the Future trait.

2. An ergonomic way of creating tasks which can be suspended and resumed through the async and await keywords.

3. A defined interface to wake up a suspended task through the Waker type.


async keyward rewrites our code block to a state machine. Each await point represents a state change.

a waker i spassed into Future::poll, iT wil hang on to thath waker

until it reaches an `await` point. when it does it will call `poll` on that future and pass the waker along

We don't actually pass a Waker directly, we pass the waker as a aprt of an object call `Context` which might add extra 
context to the poll method in the future.


Reactor just caretes an object implementing the `Future` trait and returns it.

leaf_fut.poll(waker)



## Trait object

fat pointer

```rust
use std::mem::size_of;
trait SomeTrait { }

fn main() {
    println!("======== The size of different pointers in Rust: ========");
    println!("&dyn Trait:------{}", size_of::<&dyn SomeTrait>());
    println!("&[&dyn Trait]:---{}", size_of::<&[&dyn SomeTrait]>());
    println!("Box<Trait>:------{}", size_of::<Box<SomeTrait>>());
    println!("Box<Box<Trait>>:-{}", size_of::<Box<Box<SomeTrait>>>());
    println!("&i32:------------{}", size_of::<&i32>());
    println!("&[i32]:----------{}", size_of::<&[i32]>());
    println!("Box<i32>:--------{}", size_of::<Box<i32>>());
    println!("&Box<i32>:-------{}", size_of::<&Box<i32>>());
    println!("[&dyn Trait;4]:--{}", size_of::<[&dyn SomeTrait; 4]>());
    println!("[i32;4]:---------{}", size_of::<[i32; 4]>());
}
```
The layout for a pointer to a trait object looks like this:

The first 8 bytes points to the data for the trait object
The second 8 bytes points to the vtable for the trait object


fat pointer, vtable

```rust

use std::mem::{align_of, size_of};

// A reference to a trait object is a fat pointer: (data_ptr, vtable_ptr)
trait Test {
    fn add(&self) -> i32;
    fn sub(&self) -> i32;
    fn mul(&self) -> i32;
}

// This will represent our home-brewed fat pointer to a trait object
#[repr(C)]
struct FatPointer<'a> {
    /// A reference is a pointer to an instantiated `Data` instance
    data: &'a mut Data,
    /// Since we need to pass in literal values like length and alignment it's
    /// easiest for us to convert pointers to usize-integers instead of the other way around.
    vtable: *const usize,
}

// This is the data in our trait object. It's just two numbers we want to operate on.
struct Data {
    a: i32,
    b: i32,
}

// ====== function definitions ======
fn add(s: &Data) -> i32 {
    s.a + s.b
}
fn sub(s: &Data) -> i32 {
    s.a - s.b
}
fn mul(s: &Data) -> i32 {
    s.a * s.b
}

fn main() {
    let mut data = Data {a: 3, b: 2};
    // vtable is like special purpose array of pointer-length types with a fixed
    // format where the three first values contains some general information like
    // a pointer to drop and the length and data alignment of `data`.
    let vtable = vec![
        0,                  // pointer to `Drop` (which we're not implementing here)
        size_of::<Data>(),  // length of data
        align_of::<Data>(), // alignment of data

        // we need to make sure we add these in the same order as defined in the Trait.
        add as usize, // function pointer - try changing the order of `add`
        sub as usize, // function pointer - and `sub` to see what happens
        mul as usize, // function pointer
    ];

    let fat_pointer = FatPointer { data: &mut data, vtable: vtable.as_ptr()};
    let test = unsafe { std::mem::transmute::<FatPointer, &dyn Test>(fat_pointer) };

    // And voalá, it's now a trait object we can call methods on
    println!("Add: 3 + 2 = {}", test.add());
    println!("Sub: 3 - 2 = {}", test.sub());
    println!("Mul: 3 * 2 = {}", test.mul());
}
```


std::mem::transmute


[rust generator的 RFC](https://github.com/rust-lang/rfcs/blob/master/text/2033-experimental-coroutines.md)

```rust
#[async]
fn print_lines() -> io::Result<()> {
    let addr = "127.0.0.1:8080".parse().unwrap();
    let tcp = await!(TcpStream::connect(&addr))?;
    let io = BufReader::new(tcp);

    #[async]
    for line in io.lines() {
        println!("{}", line);
    }

    Ok(())
}


fn print_lines() -> impl Future<Item = (), Error = io::Error> {
    lazy(|| {
        let addr = "127.0.0.1:8080".parse().unwrap();
        TcpStream::connect(&addr).and_then(|tcp| {
            let io = BufReader::new(tcp);

            io.lines().for_each(|line| {
                println!("{}", line);
                Ok(())
            })
        })
    })
}
```

State machines as "stackless coroutines"

```rust
fn print_lines() -> impl Future<Item = (), Error = io::Error> {
    CoroutineToFuture(|| {
        let addr = "127.0.0.1:8080".parse().unwrap();
        let tcp = {
            let mut future = TcpStream::connect(&addr);
            loop {
                match future.poll() {
                    Ok(Async::Ready(e)) => break Ok(e),
                    Ok(Async::NotReady) => yield, //这块的yield, 怎么记住state , 下次进来怎么resume ?
                    Err(e) => break Err(e),
                }
            }
        }?;

        let io = BufReader::new(tcp);

        let mut stream = io.lines();
        loop {
            let line = {
                match stream.poll()? {
                    Async::Ready(Some(e)) => e,
                    Async::Ready(None) => break,
                    Async::NotReady => {
                        yield;
                        continue
                    }
                }
            };
            println!("{}", line);
        }

        Ok(())
    })
}
```
yield 关键字:
the most prominent addition here is the usage of yield keywords. These are inserted here to inform the compiler that the coroutine should be suspended for later resumption

问题: Coroutine::resume是怎么实现的？
```rust
struct CoroutineToFuture<T>(T);

impl<T: Coroutine> Future for CoroutineToFuture {
    type Item = T::Item;
    type Error = T::Error;

    fn poll(&mut self) -> Poll<T::Item, T::Error> {
    //不知道Coroutine::resume 这个是怎么实现的
        match Coroutine::resume(&mut self.0) {
            CoroutineStatus::Return(Ok(result)) => Ok(Async::Ready(result)),
            CoroutineStatus::Return(Err(e)) => Err(e),
            CoroutineStatus::Yield => Ok(Async::NotReady),
        }
    }
}
```

设计要点

1. No implicit memory allocation
2. Coroutines are translated to state machines internally by the compiler
3. The standard library has the traits/types necessary to support the coroutines language feature.


> As a result, coroutines will roughly compile down to a state machine that's advanced forward as its resumed. Whenever a coroutine yields it'll leave itself in a state that can be later resumed from the yield statement.
这个是怎么实现的呢？



## yield关键字

```rust
#![feature(generators, generator_trait)]
use std::ops::{Generator, GeneratorState};

fn main() {
    let a: i32 = 4;
    let mut gen = move || {
        println!("Hello");
        yield a * 2;
        println!("world!");
    };

    if let GeneratorState::Yielded(n) = gen.resume() {
        println!("Got value {}", n);
    }

    if let GeneratorState::Complete(()) = gen.resume() {
        ()
    };
}
```

https://tmandry.gitlab.io/blog/posts/optimizing-await-1/




std::mem::replace 这个类似于c里面的memcp ?

std::mem::replace(self, GeneratorA::Exit
