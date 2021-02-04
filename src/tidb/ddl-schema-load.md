# Load Schema

<!-- toc -->

## Schema Cache

TiDB 使用Schema来将关系数据库中的table/index等映射到TiKV的kv存储中。

TiDB是无状态的，在TiDB内存中也加载这一份Schema, 在TiDB server中infoSchema在内存中结构如下

![model](./dot/model.svg)

## Schema Load

TiDB每隔lease/2 会去Tikv中去reload schema,
1. 首先会检查版本号，如果tikv中版本号和TiDB 中版本一致的话，就不用继续加载了, 否则进入下一步
2. `tryLoadSchemaDiffs`先尝试加载schemaDiff, 如果失败，进入下一步
3. 调用`fetchAllSchemasWithTables`会加载所有的schema

![schema-load](./dot/schema-load.svg)
