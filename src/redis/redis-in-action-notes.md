## 《Redis in Action》读书笔记
### 摘要
《Redis in action》这本书详细的介绍了redis的命令，redis中的事务，以及redis在实际工程中的应用，包括作为保存session, 购物车，访问统计的log等web开发中常见应用。

Redis中的事务是通过watch, mutl, exe的命令pipline来实现的，是个乐观锁，本书第六章介绍了在乐观锁的基础上实现的一个分布式锁（这个锁是针对单个Redis server的, 多个Redis server的可以用redis社区实现的Redlock）。

本书还介绍了一个可靠的消息队列的实现~~，(现实中通常用Rabbit MQ专门做消息队列)。

### Redis命令

#### String：字符串与数值

数值操作： incr, decr 一个不存在的key, redis会把这个key的默认值当做0来处理。

* INCR key-name 将key存储的值 +1
* DECR key-name 将key存储的值 -1
* INCRBY key-name amount 将key存储的值 + 整数amount
* DECRBY key-name amount 将key存储的值 - 整数amoun
* INCRBYFLOAT key-name amount 将可以存储的值 + 浮点数amount, 在Redis>=2.6版本可以用。

子串和二进制位操作
* APPEND key value 将value到给定key的末尾。
* GETRANGE key start end  获取 value[start, end]。
* SETRANGE key start value 将从start开始到末尾替换成value值，old_value[start, -1] = value。
* GETBIT key offset 返回二进制串中，偏移量为offset的二进制的值 value => 01010101010010101001[offset]。
* SETBIT key offset value 设置二进制串中偏移量为offset的二进制的值。
* BITCOUNT key start end 统计二进制串中值为1的二进制位的个数。
* BITOP operation dest-key key-name [key-name] 对多个二进制串做 and, or, xor,not操作, 结果保存在dest-key中。

二进制串Bitmap可以用来用户统计, 比如set yym-mm-dd:uv userid 1表示用户今天登陆了，用1M的内存可以保存838万多的用户数据, 一亿多的用户也就十几M吧。然后可以通过bittop操作，来统计任一时间段的用户活跃，然后可以用不同的bitmap表示用户的其他行为，统计的时候，只要用BITOP就可以很容易的统计各种组合了。

#### List: 列表

* RPUSH key value [value...] 将一个或多个值放到列表的右边。
* LPUSH key value [value...] 将一个或多个值放到列表的左边。
* RPOP key 移除并返回列表最右端的元素。
* LPOP key 移除并返回列表最左端的元素。
* LINDEX key index 返回列表中下标index对应的元素, list[index]。
* LRANGE key start end 返回列表中从start到end的所有元素，包括start, end, list[start, end]。
* LTRIM key start end 只保留从start到end这个范围内的元素。
* BLPOP key [key...] timeout 从第一个非空的列表中弹出最左端的元素，或者在timeout内阻塞等待。
* BRPOP key [key...] timeout 从第一个非空的列表中弹出最右端的元素，或者在timeout内阻塞等待。
* RPOPLPUSH source-key dest-key 从source-key列表中弹出最右端的元素，然后放到dest-key的最左端，并向用户返回这个元素
* BRPOPLPUSH source-key dest-key 从source-key列表中弹出最右端的元素，然后放到dest-key的最左端，并向用户返回这个元素，如果source为空那么在timeouts内会阻塞，等待可弹的元素出现。

会被block list的操作最常用于用于任务队列和消息传递。

#### Set: 集合
* SADD key item [item...] 将一个或多个元素添加到集合里面，并返回添加元素中，原本并不在结合中的元素数量。
* SREM key item [item...] 删除一个或多个元素，并返回被移除元素的数量。
* SISMEMBER key item 检查元素时候在集合中。
* SCARD key 返回集合包含元素的个数。
* SMEMBERS key 返回集合包含的所有的元素。
* SRANDMEMBER key [count] 从集合中随机抽取一个或者多个元素,count > 0：返回的元素不会重复，count < 0: 返回的元素会可能出现重复。
* SPOP key 随机从集合中移除一个元素，并返回被移除的元素。
* SMOVE source-key dest-key item 如果source-key对应的set包含item, 那么把item从sourc中移动到dest集合中。
* SDIFF key [key...] 返回存在第一集合，但不存在于其他集合的元素(差集运算)。
* SDIFFSOURCE  dest-key key [key...] 将差集运算的结果保存到dest-key对应的集合中。
* SINNER key [key...] 返回所有集合的交集。
* SINTERSTORE dest-key key [key...] 将所有集合的交集存在dest-key对应的集合中。
* SUNION key [key...] 返回所有集合的并集。
* SUNIONSTORE dest-key key [key...] 将所有几何的并集结果保存在dest-key对应的集合中。

#### Zset: 有序集合
* ZADD key score member 将给定分值的成员加到有序集合中。
* ZREM key member [member...] 从有序集合中移除给定的成员，并返回被移除的成员数量。
* ZCARD key 返回有序集合中包含的成员数量。
* ZINCRBY key increment member 将成员的分值加上increment。
* ZCOUNT key min max 返回分之介于min, max之间的成员的数量。
* ZRANK key member 返回member在有序集合中的排名。
* ZSCORE key member 返回成员member的分值。
* ZRANGE key start stop [WITHSCORES] 返回排名位于start和stop之间的成员，如果给定了withscores选项，那么分值也一起返回。
* ZREVRANK key member 返回有序集合成员member的排名，成员按照分值来排。
* ZREVRANGE key start stop [WITHSCORES] 返回有序集合给定排名范围内的成员，成员分值从大到小。
* ZRANGEBYSCORE key min max [WITHSCORES] [limit offset count] 返回有序集合中分值介于min 和max之间的所有成员。
* ZREVRANGEBYSCORE key min max [withscores] [limit offset count] 按照分值从大到小的顺序，返回有序集合中分值介于min 和max之间的所有成员。
* ZREMRANGEBYRANK key min max 移除有序集合中排名从min到max的成员。
* ZREMRANGEBYSCORE key min max 按照分值移除集合中分值介于min到max的成员。
* ZINTERSTORE dest-key key-count key [key...] [WEIGHTS weight [weight...]] 交集运算，结果保存在dest-key对应的集合中。
* ZUNIONSTORE dest-key key-count key [key...] [WEIGHTs weight [weight...]] 并集运算，结果保存在dest-key对应的集合中。

#### HashMap
* HMGET key subkey [subkey...] 从hashmap中获取一个或多个subkey对应的value
* HMSET key subkey value [subkey value ...] 为hashmap里面一个或者多个subkey设置value
* HDEL key subkey [subkey...] 删除hashmap中一个或者多个key,value, 并返回删除成功的subkey对应的value.
* HLEN key 返回hashmap包含的key,value键值对个数。
* HEXISTS key subkey 检查指定的subkey是否在hashmap中。
* HKEYS key 返回hashmap包含的所有的subkey。
* HVALS key 返回hashmap中包含的所有的values。
* HGETALL key 返回hashmap中所有的key,value键值对。
* HINCRBY key subkey amount 将subkey的值加上整数 amount。
* HINCRBYFLOAT key subkey amount 加上浮点数amount。

#### 过期
* PERSIST key 移除key的过期时间。
* TTL key  ttl(time to live) 查看给定的key距离过期还有多长时间。
* EXPIRE key seconds 让给定key在指定的秒数后过期。
* EXPIREAT key timestamp 将给定key的过期时间设置为给定的unix时间戳。
* PTTLL key 查看距离过期时间还有多少ms。
* PEXPIRE key ms 让给定的key在指定的m数以后过期，在REDIS》=2.6以上的版本可以用。
* PEXPIREAT key timestams= 设置key的失效时间戳为一个毫秒精度的unix时间戳。


#### 事务
Redis会把客户端从mult到exec之间的命令一起执行，在执行前，会检查pipeline watch的key的值是否发生了变化，如果值没变，就接着执行，变了就取消执行。

* WATCH
* MULT
* EXEC

#### 发布订阅
Redis中的订阅发布存在两个问题，一个是如果客户端处理消息速度太慢的话，会引起消息在redis output buffer中积压，会导致redis的速度变慢，也可能因为OOM导致Redis被os kill掉。新版的redis server可以通过 client-output-buffer-limit来限制缓冲区的大小。

另外一个问题是客户端如果在执行订阅操作的过程中断线，那么客户端将丢失在线期间发送的所有的消息。

* SUBSCRIBE channel [channel...]
* UNSUBSCRIBE
* PUBLISH
* PSUBSCRIBE
* PUNSUBSCRIBE

### Redis的持久化

Redis中提供了两种不同的持久化方法，一种是snapshotting, 会在某一时刻将数据都写到硬盘上，另外一种是append only file, 它会在执行写的命令的时候，将被执行的命令复制到硬盘连，append到AOF文件的后面。

#### 快照

BGSAVE命令，让redis server创建一个快照， Redis server收到BGSAVE命令后，会fork一个子进程去负责将快照写到硬盘中。如果Redis中的数据量很大比如20多个G，剩余的空闲内存也不多了，BGSAVE命令可能导致系统长时间的卡顿。根据做作者的经验。redis每占用1G内存, kvm, vmware，或者真实机器创建子进程时间就要增加10~20ms， XEN虚拟机就要增加200~300ms.

SAVE命令，redis在接到SAVE命令后，开始创建快照，并且在创建快照期间不响应任何其他命令，通常在没有足够的内存去执行BGSAVE命令的时候，才去用这个命令。

遇到SHUTDOWN或者term信号的时候，redis也会执行一个SAVE命令。

当一个Redis server连到另外一个redis server, 并发送sync命令开始执行复制操作的时候。

snapshotting方式的配置

```config
save 60 1000 //60s内有1000次写入，就自动执行BGSAVE操作。
stop-writes-on-bgsave-errors no //dumps失败后是否继续执行写命令
rbcompression yes  //进行压缩操作
dbfilename dump.rdb //快照文件名
dir ./
```

#### AOF

```ini
appendonly no
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-sze 65mb
dir ./
```

#### 主从复制: master/slaves
//TODO:
sync
pync


### Redis中的事务

redis中，客户端发送完mult命令后，redis server会把接下来的命令放到一个缓存队列中，直到读到execute命令，才开始一次执行完队列中的所有命令。由于Reids是单线程的，所以这一整块的命令都是原子性的，不会被打断。

如果执行这个命令之前，服务端会去检查客户端所watch的某个key是否发生了变化，如果发生了变化，那么这整个命令队列都不会执行。会返回WatchError。

在实现中，命令会缓存在客户端pipline中的，然后等到pipeline.execute的时候，才把所有的命令一起提交，这样能减少客户端服务端之前网络通信的次数，降低延迟值。

<img src="./images/redis-pipeline.jpeg" width="500px"/>

### 分布式锁

#### 单个Redis server

SETNX 这个命令只会在key不存在的情况下，为key设置相应的值，所以很适合拿来做lock。在acquire_lock阶段，会把lock设置为成全局唯一的uid, 然后在释放所的阶段，首先会watch自己的lock对应的id是不是自己的(这个主要是防止把别人的锁给release了，自己设定的lock已经过期了，然后lock被别的client获取了）。

这里加lock_time的原因是，防止客户端在拥有锁以后，崩溃了或者直接断开连接了，然后就永远被lock了，不过感觉这个实现有点问题，acquire_lock到release_lock之间这段执行时间不能超过lock_time，不然还是会出现race codition。    


```python
def acquire_lock(conn, lockname, acquire_timeout=10, lock_timeout=10):
    identifier = str(uuid.uuid4())
    end = time.time() + acquire_timeout
    lock = "lock:" + lockname
    lock_timeout = int(math.ceil(lock_timeout))
    while time.time() < end:
        if conn.setnx(lock, identifier):
            conn.expire(lockname, lock_timeout)
            return identifier
        elif not conn.ttl(lockname): #这个地方防止上一步stenx后，expire之前client崩溃了~~
            conn.expire(lockname, lock_timeout)
        time.sleep(0.001)
    return False

def release_lock(conn, lockname, identifier):
    pip = conn.pipline(True)
    lock = "lock:" + lockname
    while True:
        try:
            pipe.watch(lockname)
            if pip.get(lockname) == identifier:
                pipe.multi()
                pipe.delete(lockname)
                pipe.execute()
                return True
            pipe.unwatch()
        except redis.exceptions.WatchError:
            pass
    return False
```

#### 多个Redis Instance: RedLock 算法
[RedLock的实现Python](https://github.com/SPSCommerce/redlock-py/blob/master/redlock/__init__.py)
//TODO: 理解其中的细节
从N个server中获取N/2+1以上的锁才算成功~~。

### Redis 一些应用

#### Session
//Todo:

#### LiveConfig: 每个组件配置一个Redis服务

为应用程序中的每个独立部分，分别设置一个Redis server，比如说一个专门负责记录日志，一个专门负责统计数据，一个专门负责进行缓存，一个专门进行存储cookie。

这些配置信息可以存储到一个专门的Redis服务器上去。然后写个函数装饰器用于自动redis连接管理。

每隔一段时间(wait time)去检查config有没有变，如果变了就去load config，然后重新创建一个redis connection。

```python
//将redis的config信息存储到redis config server上

CONFIGS = {}
CHECKED = {}

def set_config(conn, type, component, config):
    conn.set('config:%s:%s'%(type, component), json.dumps(config))

def get_config(conn, type, component, wait=1):
    key = "config:%s:%s" %(type, component)
    if CHECKED.get(key) + wait < time.time():
        CHECKED[key] = time.time()
        config = json.loads(conn.get(key) or "{}")
        old_config = CONFIGS.get(key)
        if config != old_config:
            CONFIGS[key] = config
    return CONFIGS.get(key)
```

自动连接 Redis server
```python
REDIS_CONNECTIONS = {}
def redis_connection(component, wait=1):
    key = "config:redis:" + component
    def wrapper(function):
        @functools.warps(function):
        def call(*args, **kwargs):
            old_config = CONFIGS.get(key, object())
            _config = get_config(config_connection, 'redis', component, wait)
            config = P{}
            for k, v in _config.iteritems():
                config[k.encode("utf-8")] = v
            if config != old_config:
                REDIS_CONNECTIONS[key] = reids.Redis(**config)
            return function(REDIS_CONNECTIONS.get(key), *args, **kwargs)
        return call
    return wrapper
```

```python
@redis_connection('logs')
def log_recent(conn, app, messages):
    #log code...
    pass
```

### 参考

1. Redis in Action
2. [Distributed locks with Redis](https://redis.io/topics/distlock)
