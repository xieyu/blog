# CopTask

<!-- toc -->

## copTask

```go
// copTask contains a related Region and KeyRange for a kv.Request.
type copTask struct {
	id     uint32
	region RegionVerID
	ranges *copRanges

	respChan  chan *copResponse
	storeAddr string
	cmdType   tikvrpc.CmdType
	storeType kv.StoreType
}

// copRanges is like []kv.KeyRange, but may has extra elements at head/tail.
// It's for avoiding alloc big slice during build copTask.
type copRanges struct {
	first *kv.KeyRange
	mid   []kv.KeyRange
	last  *kv.KeyRange
}
```

## buildCopTask

## 从KeyRanges到copTask

pingcap的[TiDB 源码阅读系列文章（十九）tikv-client（下）](https://pingcap.com/blog-cn/tidb-source-code-reading-19/#tidb-%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB%E7%B3%BB%E5%88%97%E6%96%87%E7%AB%A0%E5%8D%81%E4%B9%9Dtikv-client%E4%B8%8B) 
详细介绍了distsql.

> distsql 是位于 SQL 层和 coprocessor 之间的一层抽象，它把下层的 coprocessor 请求封装起来对上层提供一个简单的 Select 方法。执行一个单表的计算任务。最上层的 SQL 语句可能会包含 JOIN，SUBQUERY 等复杂算子，涉及很多的表，而 distsql 只涉及到单个表的数据。一个 distsql 请求会涉及到多个 region，我们要对涉及到的每一个 region 执行一次 coprocessor 请求。
> 所以它们的关系是这样的，一个 SQL 语句包含多个 distsql 请求，一个 distsql 请求包含多个 coprocessor 请求。

![sql-distsql-coptask](./dot/sql-distsql-coptask.svg)


### kv.Request

```go
// Request represents a kv request.
type Request struct {
	// Tp is the request type.
	Tp        int64
	StartTs   uint64
	Data      []byte
	KeyRanges []KeyRange
  // ..
}

// KeyRange represents a range where StartKey <= key < EndKey.
type KeyRange struct {
	StartKey Key
	EndKey   Key
}

// Key represents high-level Key type.
type Key []byte
```

