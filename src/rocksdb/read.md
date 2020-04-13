# read 流程

### Questions

SuperVersion ？ 为啥起这个名字？

### 多级index:

1. ColumnFamily 根据Version中的`std::vector<FileMetaData*>` 定位到具体的Table。
2. Table根据`bloom filter`快速排出key不存在的case，如果key不存在，避免后续的磁盘操作。
3. Table根据`IndexBlock` 定位到对应的Datablock。
4. 根据Datablock数据中的`restartPoint`列表二分查找，找到对应的restartPoint偏移, 进一步缩小查找区间。
5. 在具体的`restartPoint`之间遍历查找具体的key

![table read index](./table_read_index.svg)

### 多级LRU缓存:

1. TableCache
2. DataBlockCache
3. RowCache

![table read cache](./table_read_cache.svg)

详细调用关系：

![db impl get](./dbimpl_get.svg)
