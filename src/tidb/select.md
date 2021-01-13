# Select 语句

<!-- toc -->

## SelectStmt

```go
type SelectStmt struct {
	dmlNode
	resultSetNode

	// SelectStmtOpts wraps around select hints and switches.
	*SelectStmtOpts
	// Distinct represents whether the select has distinct option.
	Distinct bool
	// From is the from clause of the query.
	From *TableRefsClause
	// Where is the where clause in select statement.
	Where ExprNode
	// Fields is the select expression list.
	Fields *FieldList
	// GroupBy is the group by expression list.
	GroupBy *GroupByClause
	// Having is the having condition.
	Having *HavingClause
	// WindowSpecs is the window specification list.
	WindowSpecs []WindowSpec
	// OrderBy is the ordering expression list.
	OrderBy *OrderByClause
	// Limit is the limit clause.
	Limit *Limit
	// LockInfo is the lock type
	LockInfo *SelectLockInfo
	// TableHints represents the table level Optimizer Hint for join type
	TableHints []*TableOptimizerHint
	// IsInBraces indicates whether it's a stmt in brace.
	IsInBraces bool
	// QueryBlockOffset indicates the order of this SelectStmt if counted from left to right in the sql text.
	QueryBlockOffset int
	// SelectIntoOpt is the select-into option.
	SelectIntoOpt *SelectIntoOption
	// AfterSetOperator indicates the SelectStmt after which type of set operator
	AfterSetOperator *SetOprType
	// Kind refer to three kind of statement: SelectStmt, TableStmt and ValuesStmt
	Kind SelectStmtKind
	// Lists is filled only when Kind == SelectStmtKindValues
	Lists []*RowExpr
}
```

## LogicalPlan

![build select plan](./dot/build_select_plan.svg)


## PhysicalPlan

### DataSource.findBestTask

![data source findBestTask](./dot/datasource-findbesttask.svg)

### LogicalJoin.exhaustPhysicalPlans

![logicaljoin exhaustPhysicalPlans](./dot/logicaljoin_exhaustPhysicalPlans.svg)

## Executor

### SelectionExec

```
// SelectionExec represents a filter executor.
type SelectionExec struct {
	baseExecutor

	batched     bool
	filters     []expression.Expression
	selected    []bool
	inputIter   *chunk.Iterator4Chunk
	inputRow    chunk.Row
	childResult *chunk.Chunk

	memTracker *memory.Tracker
}
```

生成的计划
```sql
explain select name, age from t where id = 'pingcap';

+-----------------------+---------+-----------+---------------+--------------------------------+
| id                    | estRows | task      | access object | operator info                  |
+-----------------------+---------+-----------+---------------+--------------------------------+
| Projection_4          | 0.00    | root      |               | tests.t.name, tests.t.age      |
| └─TableReader_7       | 0.00    | root      |               | data:Selection_6               |
|   └─Selection_6       | 0.00    | cop[tikv] |               | eq(tests.t.id, "pingcap")      |
|     └─TableFullScan_5 | 3.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+-----------------------+---------+-----------+---------------+--------------------------------+
```
