# TiDB Server Main Loop

<!-- toc -->

跟着官方的[tidb源码阅读博客](https://pingcap.com/blog-cn/tidb-source-code-reading-3/)，看了TiDB main函数，大致了解了一个SQL的处理过程

## conn session

下图显示了TiDB中Accept一个mysql连接的处理流程，对于每个新的conn, TiDB会启动一个goroutine来处理这个conn, 并按照Mysql协议，处理不同的mysql cmd。
每个conn在server端会有个对应的session.

对于Query语句，会session.Execute生成一个执行器，返回一个resultSet, 最后调用``writeResultset``, 从ResultSet.Next中获取结果，然后将结果返回给客户端。

![tidb server main](./dot/tidb-server-main.svg)

一个sql语句执行过程中经过以下几个过程:

1. `ParseSQL` 将SQL语句解析为stmt ast tree
2. `Compile` 将stmt ast tree 转换为physical plan
3. `BuildExecutor` 创建executor
4. `resultSet.Next` 驱动executor执行

![sql-to-resultset](./dot/sql-to-resultset.svg)

## ParseSQL

### StmtNodes

StmtNode 接口定义
```go
// Node is the basic element of the AST.
// Interfaces embed Node should have 'Node' name suffix.
type Node interface {
	// Restore returns the sql text from ast tree
	Restore(ctx *format.RestoreCtx) error
	// Accept accepts Visitor to visit itself.
	// The returned node should replace original node.
	// ok returns false to stop visiting.
	//
	// Implementation of this method should first call visitor.Enter,
	// assign the returned node to its method receiver, if skipChildren returns true,
	// children should be skipped. Otherwise, call its children in particular order that
	// later elements depends on former elements. Finally, return visitor.Leave.
	Accept(v Visitor) (node Node, ok bool)
	// Text returns the original text of the element.
	Text() string
	// SetText sets original text to the Node.
	SetText(text string)
}

// StmtNode represents statement node.
// Name of implementations should have 'Stmt' suffix.
type StmtNode interface {
	Node
	statement()
}
```

stmtNode实现种类和继承关系

![stmt-nodes](./dot/stmt-nodes.svg)

## Compile


![sql-plan](./dot/sql-plan.svg)

### logical plan optimize

```go
var optRuleList = []logicalOptRule{
	&gcSubstituter{},
	&columnPruner{},
	&buildKeySolver{},
	&decorrelateSolver{},
	&aggregationEliminator{},
	&projectionEliminator{},
	&maxMinEliminator{},
	&ppdSolver{},
	&outerJoinEliminator{},
	&partitionProcessor{},
	&aggregationPushDownSolver{},
	&pushDownTopNOptimizer{},
	&joinReOrderSolver{},
	&columnPruner{}, // column pruning again at last, note it will mess up the results of buildKeySolver
}
```

### task

task分为rooTask和copTask, rootTask在TIDB端执行，
copTask在kv层执行

#### rootTask
```go
// rootTask is the final sink node of a plan graph. It should be a single goroutine on tidb.
type rootTask struct {
	p   PhysicalPlan
	cst float64
}
```

#### copTask 
```go
// copTask is a task that runs in a distributed kv store.
// TODO: In future, we should split copTask to indexTask and tableTask.
type copTask struct {
	indexPlan PhysicalPlan
	tablePlan PhysicalPlan
	cst       float64
	// indexPlanFinished means we have finished index plan.
	indexPlanFinished bool
	// keepOrder indicates if the plan scans data by order.
	keepOrder bool
	// doubleReadNeedProj means an extra prune is needed because
	// in double read case, it may output one more column for handle(row id).
	doubleReadNeedProj bool

	extraHandleCol   *expression.Column
	commonHandleCols []*expression.Column
	// tblColHists stores the original stats of DataSource, it is used to get
	// average row width when computing network cost.
	tblColHists *statistics.HistColl
	// tblCols stores the original columns of DataSource before being pruned, it
	// is used to compute average row width when computing scan cost.
	tblCols           []*expression.Column
	idxMergePartPlans []PhysicalPlan
	// rootTaskConds stores select conditions containing virtual columns.
	// These conditions can't push to TiKV, so we have to add a selection for rootTask
	rootTaskConds []expression.Expression

	// For table partition.
	partitionInfo PartitionInfo
}
```

### ExecStmt

```go
// ExecStmt implements the sqlexec.Statement interface, it builds a planner.Plan to an sqlexec.Statement.
type ExecStmt struct {
	// GoCtx stores parent go context.Context for a stmt.
	GoCtx context.Context
	// InfoSchema stores a reference to the schema information.
	InfoSchema infoschema.InfoSchema
	// Plan stores a reference to the final physical plan.
	Plan plannercore.Plan
	// Text represents the origin query text.
	Text string

	StmtNode ast.StmtNode

	Ctx sessionctx.Context

	// LowerPriority represents whether to lower the execution priority of a query.
	LowerPriority     bool
	isPreparedStmt    bool
	isSelectForUpdate bool
	retryCount        uint
	retryStartTime    time.Time

	// OutputNames will be set if using cached plan
	OutputNames []*types.FieldName
	PsStmt      *plannercore.CachedPrepareStmt
}
```


## build executor

根据plan生成相应的executor


![sql-executor](./sql-executor.svg)

Executor interface如下, 使用了Volcano模型，接口用起来和迭代器差不多，采用Open-Next-Close套路来使用。
```go
// Executor is the physical implementation of a algebra operator.
//
// In TiDB, all algebra operators are implemented as iterators, i.e., they
// support a simple Open-Next-Close protocol. See this paper for more details:
//
// "Volcano-An Extensible and Parallel Query Evaluation System"
//
// Different from Volcano's execution model, a "Next" function call in TiDB will
// return a batch of rows, other than a single row in Volcano.
// NOTE: Executors must call "chk.Reset()" before appending their results to it.
type Executor interface {
	base() *baseExecutor
	Open(context.Context) error
	Next(ctx context.Context, req *chunk.Chunk) error
	Close() error
	Schema() *expression.Schema
}
```

### executor Next

#### handleNoDelay

不需要返回结果的立即执行

![sql-nodelay-next](./sql-nodelay-next.svg)

#### RecordSet driver

![sql-recordset-driver](./sql-recordset-driver.svg)

```go
// RecordSet is an abstract result set interface to help get data from Plan.
type RecordSet interface {
	// Fields gets result fields.
	Fields() []*ast.ResultField

	// Next reads records into chunk.
	Next(ctx context.Context, req *chunk.Chunk) error

	// NewChunk create a chunk.
	NewChunk() *chunk.Chunk

	// Close closes the underlying iterator, call Next after Close will
	// restart the iteration.
	Close() error
}
```

RecordSet Next方法接口的实现.
```go
// Next use uses recordSet's executor to get next available chunk for later usage.
// If chunk does not contain any rows, then we update last query found rows in session variable as current found rows.
// The reason we need update is that chunk with 0 rows indicating we already finished current query, we need prepare for
// next query.
// If stmt is not nil and chunk with some rows inside, we simply update last query found rows by the number of row in chunk.
func (a *recordSet) Next(ctx context.Context, req *chunk.Chunk) error {
	err := Next(ctx, a.executor, req)
	if err != nil {
		a.lastErr = err
		return err
	}
	numRows := req.NumRows()
	if numRows == 0 {
		if a.stmt != nil {
			a.stmt.Ctx.GetSessionVars().LastFoundRows = a.stmt.Ctx.GetSessionVars().StmtCtx.FoundRows()
		}
		return nil
	}
	if a.stmt != nil {
		a.stmt.Ctx.GetSessionVars().StmtCtx.AddFoundRows(uint64(numRows))
	}
	return nil
}
```

在writeResult时候不断调用RecordSet的Next方法，去驱动调用executor的Next;

```go
// writeChunks writes data from a Chunk, which filled data by a ResultSet, into a connection.
// binary specifies the way to dump data. It throws any error while dumping data.
// serverStatus, a flag bit represents server information
func (cc *clientConn) writeChunks(ctx context.Context, rs ResultSet, binary bool, serverStatus uint16) error {
	data := cc.alloc.AllocWithLen(4, 1024)
	req := rs.NewChunk()
  //...
	for {
		// Here server.tidbResultSet implements Next method.
		err := rs.Next(ctx, req)
    /...
		rowCount := req.NumRows()
    //...
		for i := 0; i < rowCount; i++ {
			data = data[0:4]
      /...
			if err = cc.writePacket(data); err != nil {
				return err
			}
      //...
    }
  }
	return cc.writeEOF(serverStatus)
}
```


