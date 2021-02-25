# buildDataSource

<!-- toc -->

<!-- ![](./dot/buildDataSource.svg) -->
## TableByName
根据tableName，找到对应的tableInfo

![](./dot/TableByName.svg)

## Schema

![](./dot/buildDataSource-schema.svg)

## handleCols

![](./dot/buildDataSource-handleCols.svg)

## getPossibleAccessPaths

遍历table的Indices, 生成对应的AccessPath

![](./dot/buildDataSource-getPossibleAccessPath.svg)
