## Glibc的pthread实现代码阅读

本文主要包含两个部分，第一部分 ``thread lifecycle`` 主要讲述 Glibc pthread实现中的线程的生命周期，主要包含线程的创建，执行，exit, detach和join。

第二部分主要讲述pthread中的线程的同步方法包括Mutex, Sem, Condvar, Barrier的实现，pthread使用了linux的futex来实现。

### thread lifecycle

#### pthread_create

pthread create 主要做了如下几个工作:

1. 分配stack, 使用用户提供的stack或者系统分配一个stack(pd 这个struct也存放在stack里面了)
```cpp
ALLOCATE_STACK(iattr, &pd)
```

2. ``create_thread`` 调用linux系统接口clone创建线程, 如果线程要指定在某个CPU上跑的话，调用sched_setaffinity设置好cpuset, 最后何止好调度策略和调度参数。

```cpp
ARCH_CLONE(&start_thread, STACK_VARIABLES_ARGS, clone_flags, pd, &pd->tid, tp, &pd->tid)

INTERNAL_SYSCALL(sched_setaffinity, err, 3, pd->tid, attr->cpusetsize, attr->cpuset)

INTERNAL_SYSCALL(sched_setscheduler, err, 3, pd->tid, pd->schedpolicy, &pd->schedparam)
```

其中clone 的flags如下：
```cpp
const int clone_flags = (CLONE_VM | CLONE_FS | CLONE_FILES | CLONE_SYSVSEM
              | CLONE_SIGHAND | CLONE_THREAD
              | CLONE_SETTLS | CLONE_PARENT_SETTID
              | CLONE_CHILD_CLEARTID
              | 0);
```

``CLONE_THREAD``, 标明是创建一个线程，和创建者同一个group,  同一个parent。

 ``STACK_VARIABLES_ARGS``对应着上一步ALLOCATE_STACK分配好的内存地址, 这块内存会作为新的线程的stack来用。

clone中的的start_thread就是线程的entry_point, 这个函数定义在nptl/pthread_create.c里面 ``START_THREAD_DEFF``, 这个函数就是新创建的线程的入口。

#### start thread

1. 设置好unwind_buf

```cpp
int not_first_call;
 not_first_call = setjmp ((struct __jmp_buf_tag *) unwind_buf.cancel_jmp_buf);
 if (__glibc_likely (! not_first_call))
   {
     /* Store the new cleanup handler info.  */
     THREAD_SETMEM (pd, cleanup_jmp_buf, &unwind_buf);

```
setjmp和longjmp是非局部跳转函数, 它可以在在栈上跳过若干调用帧，返回到当前函数调用路径上的某一个函数中, 若直接调用则返回0，若从longjmp调用返回则返回非0值的longjmp中的val值。


2. 调用用户提供的函数, 结果存在``pd->result``中

```cpp
#ifdef CALL_THREAD_FCT
      THREAD_SETMEM (pd, result, CALL_THREAD_FCT (pd));
#else
      THREAD_SETMEM (pd, result, pd->start_routine (pd->arg));
#endif
```

3. 清理TLS, 标记stack为可复用状态，如果线程是detached, 则释放pd的内存。

```cpp
__call_tls_dtors ();
/* Run the destructor for the thread-local data.  */
__nptl_deallocate_tsd ();
/* Clean up any state libc stored in thread-local variables.  */
__libc_thread_freeres ();
if (IS_DETACHED (pd))
    __free_tcb (pd);

// mark stack resuable
char *sp = CURRENT_STACK_FRAME;
size_t freesize = (sp - (char *) pd->stackblock) & ~pagesize_m1;
assert (freesize < pd->stackblock_size);
if (freesize > PTHREAD_STACK_MIN)
  __madvise (pd->stackblock, freesize - PTHREAD_STACK_MIN, MADV_DONTNEED);

// other code
__exit_thread ();
```

#### pthread_exit
猜测pthread_exit 的do_canel 里面会longjmp回到start_thread里面的setjmp那块，继续执行线程结束后的清理工作。

```cpp
__pthread_exit (void *value)
{
  THREAD_SETMEM (THREAD_SELF, result, value);

  __do_cancel ();
}
```

do_cancel定义如下:
```cpp
__do_cancel (void)
{
  struct pthread *self = THREAD_SELF;

  THREAD_ATOMIC_BIT_SET (self, cancelhandling, EXITING_BIT);
  __pthread_unwind ((__pthread_unwind_buf_t *)
		    THREAD_GETMEM (self, cleanup_jmp_buf));
}

```

#### pthread_join

``pthread_join(t1, &result)`` 线程会等到t1执行结束，然后从result获取线程返回的结果。

1. 检查是否有死锁,(避免出现自己等待自己的状况)(TODO:弄清楚这块的CANCEL_BITMASK)

```cpp
if ((pd == self
       || (self->joinid == pd
	   && (pd->cancelhandling
	       & (CANCELING_BITMASK | CANCELED_BITMASK | EXITING_BITMASK
		  | TERMINATED_BITMASK)) == 0))
      && !CANCEL_ENABLED_AND_CANCELED (self->cancelhandling))
result = EDEADLK;
```

2. 设置``t1->joinid = self;``
```cpp
/* Wait for the thread to finish.  If it is already locked something
     is wrong.  There can only be one waiter.  */
  else if (__builtin_expect (atomic_compare_and_exchange_bool_acq (&pd->joinid,
								   self,
								   NULL), 0))
    /* There is already somebody waiting for the thread.  */
    result = EINVAL;
```

3. 等待t1线程执行结束, 这里的lll_wait_tid 最后会去调用linux提供的futex, 会被挂起来，一直等到t1的tid变为0。

```cpp
else
    /* Wait for the child.  */
    lll_wait_tid (pd->tid);
```

4. free t1线程的pd struct
```
pd->tid = -1;

     /* Store the return value if the caller is interested.  */
     if (thread_return != NULL)
   *thread_return = pd->result;


     /* Free the TCB.  */
     __free_tcb (pd);
```

#### pthread_detach

标记线程为detached, 如果线程是cancel状态就是释放pd struct对应的内存(TODO:弄清楚EXITING_BITMASK这个)

```cpp
  int result = 0;
  /* Mark the thread as detached.  */
  if (atomic_compare_and_exchange_bool_acq (&pd->joinid, pd, NULL))
    {
      if (IS_DETACHED (pd))
	      result = EINVAL;
    }
  else if ((pd->cancelhandling & EXITING_BITMASK) != 0)
      __free_tcb (pd);
  return result;

```


### 线程的同步

pthread中的locks通过linux的futex(faster user space locking)实现, lock放在process之间的共享内存中, pthread通过atomic的指令来对这个lock进行dec, inc, load and test 等操作, 如果有竞态冲突的时候获取锁失败的时候，才会去sys call 调用linux底层的do_futex, 底层把线程放到futex对应的wait队列里面, 然后挂起线程等待被唤醒。

由于只有竞态冲突的时候才需要syscall, 其他情况都不需要，因此节省了很多sys call，这样比较快。

<img src="./glibc-pthread-images/pthread-lock-overview.jpeg" width=300px/>



#### Mutex
xchgl 这个是atomic操作吧，失败了回去调用do_futex, flag 是FUTEX_WAIT

```
phtread_mutex_lock --> LL_MUTEX_LOCK --> ll_lock --> lll_lock_wait|lll_lock_wait_private --> xchgl

```

#### Sem

#### Condition var

#### Read write lock

#### Barrier
