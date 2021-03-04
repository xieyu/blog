# DataSource

<!-- toc -->

## Logical Plan

DataSource在query plan tree中是叶子节点，表示数据来源，在Logical Plan Optimize中，查询过滤条件
会尽量向叶子节点下推。

下推的过滤条件conds，首先被用于分区剪枝(根据partion expr相关的cond剪枝)，
然后primary key相关的cond会被抽出来，转换成为TiKV层Range。

最后其他无法抽离出来的cond被下推到TiKV层, 由TiKV层coprocessor来处理。

### struct DataSource

`DataSource` 中的`tableInfo`字段包含了table的一些元信息，比如
tableId, indices之类的。

``possibleAccessPaths``表示该DataSource的所有
可能访问路径，比如TableScan 或者扫描某个index等。

``TblColHists`` 用来Estimate符合条件的RowCount,  从而估算对应physical plan的cost.

![](./dot/datasource.svg)

```go
// DataSource represents a tableScan without condition push down.
type DataSource struct {
	logicalSchemaProducer

	astIndexHints []*ast.IndexHint
	IndexHints    []indexHintInfo
	table         table.Table
	tableInfo     *model.TableInfo
	Columns       []*model.ColumnInfo
	DBName        model.CIStr

	TableAsName *model.CIStr
	// indexMergeHints are the hint for indexmerge.
	indexMergeHints []indexHintInfo
	// pushedDownConds are the conditions that will be pushed down to coprocessor.
	pushedDownConds []expression.Expression
	// allConds contains all the filters on this table. For now it's maintained
	// in predicate push down and used only in partition pruning.
	allConds []expression.Expression

	statisticTable *statistics.Table
	tableStats     *property.StatsInfo

	// possibleAccessPaths stores all the possible access path for physical plan, including table scan.
	possibleAccessPaths []*util.AccessPath

	// The data source may be a partition, rather than a real table.
	isPartition     bool
	physicalTableID int64
	partitionNames  []model.CIStr

	// handleCol represents the handle column for the datasource, either the
	// int primary key column or extra handle column.
	//handleCol *expression.Column
	handleCols HandleCols
	// TblCols contains the original columns of table before being pruned, and it
	// is used for estimating table scan cost.
	TblCols []*expression.Column
	// commonHandleCols and commonHandleLens save the info of primary key which is the clustered index.
	commonHandleCols []*expression.Column
	commonHandleLens []int
	// TblColHists contains the Histogram of all original table columns,
	// it is converted from statisticTable, and used for IO/network cost estimating.
	TblColHists *statistics.HistColl
	// preferStoreType means the DataSource is enforced to which storage.
	preferStoreType int
	// preferPartitions store the map, the key represents store type, the value represents the partition name list.
	preferPartitions map[int][]model.CIStr
}
```
### AccessPath
AccessPath 表示我们访问一个table路径，是基于单索引，还是使用多索引, 或者去扫描整个表，其定义如下,
在逻辑优化阶段的paritionProcessor中会生成DataSource的所有possiableAccessPath

```go
type AccessPath struct {
	Index          *model.IndexInfo
	FullIdxCols    []*expression.Column
	FullIdxColLens []int
	IdxCols        []*expression.Column
	IdxColLens     []int
	Ranges         []*ranger.Range
	// CountAfterAccess is the row count after we apply range seek and before we use other filter to filter data.
	// For index merge path, CountAfterAccess is the row count after partial paths and before we apply table filters.
	CountAfterAccess float64
	// CountAfterIndex is the row count after we apply filters on index and before we apply the table filters.
	CountAfterIndex float64
	AccessConds     []expression.Expression
	EqCondCount     int
	EqOrInCondCount int
	IndexFilters    []expression.Expression
	TableFilters    []expression.Expression
	// PartialIndexPaths store all index access paths.
	// If there are extra filters, store them in TableFilters.
	PartialIndexPaths []*AccessPath

	StoreType kv.StoreType

	IsDNFCond bool

	// IsTiFlashGlobalRead indicates whether this path is a remote read path for tiflash
	IsTiFlashGlobalRead bool

	// IsIntHandlePath indicates whether this path is table path.
	IsIntHandlePath    bool
	IsCommonHandlePath bool
	// Forced means this path is generated by `use/force index()`.
	Forced bool
}
```