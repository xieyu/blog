# Schema 存储
<!-- toc -->

## Schema 存储格式

Schema在kv中的存储形式如下

```go
//meta/meta.go // Meta structure:
//	NextGlobalID -> int64
//	SchemaVersion -> int64
//	DBs -> {
//		DB:1 -> db meta data []byte
//		DB:2 -> db meta data []byte
//	}
//	DB:1 -> {
//		Table:1 -> table meta data []byte
//		Table:2 -> table meta data []byte
//		TID:1 -> int64
//		TID:2 -> int64
//	}
//
```

## meta

TiDB `meta/meta.go`模块封装了对存储在TiKV中schema进行的操作

1. ddl owner节点在 `runDDLJobs`时候，会调用meta的方法修改schema。
2. TiDB `loadSchemaInLoop` 中调用meta方法来加载schema.

模块层次之间调用如下图所示:

![schema mata](./dot/schema-meta.svg)


```go
// Meta is for handling meta information in a transaction.
type Meta struct {
	txn        *structure.TxStructure
	StartTS    uint64 // StartTS is the txn's start TS.
	jobListKey JobListKeyType
}

// TxStructure supports some simple data structures like string, hash, list, etc... and
// you can use these in a transaction.
type TxStructure struct {
	reader     kv.Retriever
	readWriter kv.RetrieverMutator
	prefix     []byte
}

// RetrieverMutator is the interface that groups Retriever and Mutator interfaces.
type RetrieverMutator interface {
	Retriever
	Mutator
}

// Getter is the interface for the Get method.
type Getter interface {
	// Get gets the value for key k from kv store.
	// If corresponding kv pair does not exist, it returns nil and ErrNotExist.
	Get(ctx context.Context, k Key) ([]byte, error)
}
// Retriever is the interface wraps the basic Get and Seek methods.
type Retriever interface {
	Getter
	// Iter creates an Iterator positioned on the first entry that k <= entry's key.
	// If such entry is not found, it returns an invalid Iterator with no error.
	// It yields only keys that < upperBound. If upperBound is nil, it means the upperBound is unbounded.
	// The Iterator must be Closed after use.
	Iter(k Key, upperBound Key) (Iterator, error)

	// IterReverse creates a reversed Iterator positioned on the first entry which key is less than k.
	// The returned iterator will iterate from greater key to smaller key.
	// If k is nil, the returned iterator will be positioned at the last key.
	// TODO: Add lower bound limit
	IterReverse(k Key) (Iterator, error)
}

// Mutator is the interface wraps the basic Set and Delete methods.
type Mutator interface {
	// Set sets the value for key k as v into kv store.
	// v must NOT be nil or empty, otherwise it returns ErrCannotSetNilValue.
	Set(k Key, v []byte) error
	// Delete removes the entry for key k from kv store.
	Delete(k Key) error
}
```
