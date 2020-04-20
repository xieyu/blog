# Blob

Questions:
1. PinnableSlice 这个作用是啥
2. rocksdb的blob和pingcap的titan之间关系？实现逻辑？
5. Blob文件是怎么选择的

Blob将key和value分来开存储。
```cpp
// A wrapped database which puts values of KV pairs in a separate log
// and store location to the log in the underlying DB.
```

![blob db](./blob-db.svg)

## Blob Log
blob log format

![blob log format](./blob-log-format.svg)

blob index

![blob index](./blob-index.svg)

## Open

Blob open
![blob open](./blob-open.svg)


## Put
BlobPut

![blob put](./blob-put.svg)

## Get
BlobGet
![blob get](./blob-get.svg)

