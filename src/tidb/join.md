# Join

<!-- toc -->

## Join算法

### Nest loop join
`nest loop join`, 遍历取外表R中一条记录r, 然后遍历inner表S每条记录和r做join。
对于外表中的每一条记录，都需要对Inner表做一次全表扫描。IO比较高

```
algorithm nested_loop_join is
    for each tuple r in R do
        for each tuple s in S do
            if r and s satisfy the join condition then
                yield tuple <r,s>
```

### Block nest loop join

Block Nest Loop Join是对NestLoop Join的一个优化

```
for each block Br of r do begin
  for each block Bs of s do begin
    for each tuple tr in Br do begin
      for each tuple ts in Bs do begin
        test pair (tr, ts) to see if they satisfy the join condition
          if they do, add tr ⋅ ts to the result;
      end
    end
  end
end
```

### Indexed Nested loop join

`index join` inner表中对于要join的attribute由了索引, 可以使用索引
来避免对inner表的全表扫描, 复杂度为`O(M * log N)`

```
for each tuple r in R do
    for each tuple s in S in the index lookup do
        yield tuple <r,s>
```

### Sort Merge Join

```
function sortMerge(relation left, relation right, attribute a)
    var relation output
    var list left_sorted := sort(left, a) // Relation left sorted on attribute a
    var list right_sorted := sort(right, a)
    var attribute left_key, right_key
    var set left_subset, right_subset // These sets discarded except where join predicate is satisfied
    advance(left_subset, left_sorted, left_key, a)
    advance(right_subset, right_sorted, right_key, a)
    while not empty(left_subset) and not empty(right_subset)
        if left_key = right_key // Join predicate satisfied
            add cartesian product of left_subset and right_subset to output
            advance(left_subset, left_sorted, left_key, a)
            advance(right_subset, right_sorted,right_key, a)
        else if left_key < right_key
            advance(left_subset, left_sorted, left_key, a)
        else // left_key > right_key
            advance(right_subset, right_sorted, right_key, a)
    return output

// Remove tuples from sorted to subset until the sorted[1].a value changes
function advance(subset out, sorted inout, key out, a in)
    key := sorted[1].a
    subset := emptySet
    while not empty(sorted) and sorted[1].a = key
        insert sorted[1] into subset
        remove sorted[1] 
```



### Hash join

```pascal
/* Partition s */
for each tuple ts in s do begin
  i := h(ts[JoinAttrs]);
  Hsi := Hsi ∪ {ts};
end

/* Partition r */
for each tuple tr in r do begin
  i := h(tr[JoinAttrs]);
  Hri := Hri ∪ {tr};
end

/* Perform join on each partition */
for i := 0 to nh do begin
  read Hsi and build an in-memory hash index on it;
  for each tuple tr in Hri do begin
    probe the hash index on Hsi to locate all tuples ts
    such that ts[JoinAttrs] = tr[JoinAttrs];
    for each matching tuple ts in Hsi do begin
      add tr ⋈ ts to the result;
    end
  end
end
```

## Logical Optimize

### join reorder

## Physical Optimize

### Physical Join 继承关系

![](./dot/physical-join-inherit.svg)

### Physical PhysicalProperty

![](./dot/physical-property.svg)

```go
// It contains the orders and the task types.
type PhysicalProperty struct {
	Items []Item

	// TaskTp means the type of task that an operator requires.
	//
	// It needs to be specified because two different tasks can't be compared
	// with cost directly. e.g. If a copTask takes less cost than a rootTask,
	// we can't sure that we must choose the former one. Because the copTask
	// must be finished and increase its cost in sometime, but we can't make
	// sure the finishing time. So the best way to let the comparison fair is
	// to add TaskType to required property.
	TaskTp TaskType

	// ExpectedCnt means this operator may be closed after fetching ExpectedCnt
	// records.
	ExpectedCnt float64

	// hashcode stores the hash code of a PhysicalProperty, will be lazily
	// calculated when function "HashCode()" being called.
	hashcode []byte

	// whether need to enforce property.
	Enforced bool
}
```

#### taskType
```go
// TaskType is the type of execution task.
type TaskType int

const (
	// RootTaskType stands for the tasks that executed in the TiDB layer.
	RootTaskType TaskType = iota

	// CopSingleReadTaskType stands for the a TableScan or IndexScan tasks
	// executed in the coprocessor layer.
	CopSingleReadTaskType

	// CopDoubleReadTaskType stands for the a IndexLookup tasks executed in the
	// coprocessor layer.
	CopDoubleReadTaskType

	// CopTiFlashLocalReadTaskType stands for flash coprocessor that read data locally,
	// and only a part of the data is read in one cop task, if the current task type is
	// CopTiFlashLocalReadTaskType, all its children prop's task type is CopTiFlashLocalReadTaskType
	CopTiFlashLocalReadTaskType

	// CopTiFlashGlobalReadTaskType stands for flash coprocessor that read data globally
	// and all the data of given table will be read in one cop task, if the current task
	// type is CopTiFlashGlobalReadTaskType, all its children prop's task type is
	// CopTiFlashGlobalReadTaskType
	CopTiFlashGlobalReadTaskType
)
```

### findBestTask

枚举所有满足parent plan physicalProperty 的join物理计划, 其中GetMergeJoin, 给child加了PhyscialProp 要求child plan是按照joinKey 降序排序.

```go
// LogicalJoin can generates hash join, index join and sort merge join.
// Firstly we check the hint, if hint is figured by user, we force to choose the corresponding physical plan.
// If the hint is not matched, it will get other candidates.
// If the hint is not figured, we will pick all candidates.
func (p *LogicalJoin) exhaustPhysicalPlans(prop *property.PhysicalProperty) ([]PhysicalPlan, bool) {
//...
}
```

![logicaljoin exhaustPhysicalPlans](./dot/logicaljoin_exhaustPhysicalPlans.svg)

估算每个join计划的cost

![](./dot/physical-join-cost.svg)

#### PhysicalMergeJoin

```go
func (p *PhysicalMergeJoin) attach2Task(tasks ...task) task {
	lTask := finishCopTask(p.ctx, tasks[0].copy())
	rTask := finishCopTask(p.ctx, tasks[1].copy())
	p.SetChildren(lTask.plan(), rTask.plan())
	return &rootTask{
		p:   p,
		cst: lTask.cost() + rTask.cost() + p.GetCost(lTask.count(), rTask.count()),
	}
}
```
#### PhysicalHashJoin

```go
func (p *PhysicalHashJoin) attach2Task(tasks ...task) task {
	lTask := finishCopTask(p.ctx, tasks[0].copy())
	rTask := finishCopTask(p.ctx, tasks[1].copy())
	p.SetChildren(lTask.plan(), rTask.plan())
	task := &rootTask{
		p:   p,
		cst: lTask.cost() + rTask.cost() + p.GetCost(lTask.count(), rTask.count()),
	}
	return task
}
```

#### PhysicalIndexJoin

```go
func (p *PhysicalIndexJoin) attach2Task(tasks ...task) task {
	innerTask := p.innerTask
	outerTask := finishCopTask(p.ctx, tasks[1-p.InnerChildIdx].copy())
	if p.InnerChildIdx == 1 {
		p.SetChildren(outerTask.plan(), innerTask.plan())
	} else {
		p.SetChildren(innerTask.plan(), outerTask.plan())
	}
	return &rootTask{
		p:   p,
		cst: p.GetCost(outerTask, innerTask),
	}
}
```



## Executors

### MergeJoinExec

![](./dot/merge-join-struct.svg)

参考资料[TiDB 源码阅读系列文章（十五）Sort Merge Join](https://pingcap.com/blog-cn/tidb-source-code-reading-15/)

fetchNextInnerGroup
和fetchNextOuterGroup的区别是啥

```go
// MergeJoinExec implements the merge join algorithm.
// This operator assumes that two iterators of both sides
// will provide required order on join condition:
// 1. For equal-join, one of the join key from each side
// matches the order given.
// 2. For other cases its preferred not to use SMJ and operator
// will throw error.
type MergeJoinExec struct {
	baseExecutor

	stmtCtx      *stmtctx.StatementContext
	compareFuncs []expression.CompareFunc
	joiner       joiner
	isOuterJoin  bool
	desc         bool

	innerTable *mergeJoinTable
	outerTable *mergeJoinTable

	hasMatch bool
	hasNull  bool

	memTracker  *memory.Tracker
	diskTracker *disk.Tracker
}
```



首先使用vecGroupCheck分别将innner chunk和outerchunk 分为相同groupkey的组

![merge join exec](./dot/merge-join.svg)

### HashJoinExec


[TiDB 源码阅读系列文章（九）Hash Join](https://pingcap.com/blog-cn/tidb-source-code-reading-9/)

```go
// step 1. fetch data from build side child and build a hash table;
// step 2. fetch data from probe child in a background goroutine and probe the hash table in multiple join workers.
```
![hash join](./dot/hash-join.svg) 

### IndexLookUpJoin

参考资料
1. [TiDB 源码阅读系列文章（十一）Index Lookup Join](https://pingcap.com/blog-cn/tidb-source-code-reading-11/)
2. [wikipedia: Nested_loop_join](https://en.wikipedia.org/wiki/Nested_loop_join)


根据[TiDB 源码阅读系列文章（十一）Index Lookup Join](https://pingcap.com/blog-cn/tidb-source-code-reading-11/)中介绍，其实现思路主要如下：

1. 从 Outer 表中取一批数据，设为 B；
2. 通过 Join Key 以及 B 中的数据构造 Inner 表取值范围，只读取对应取值范围的数据，设为 S；
3. 对 B 中的每一行数据，与 S 中的每一条数据执行 Join 操作并输出结果；
4. 重复步骤 1，2，3，直至遍历完 Outer 表中的所有数据。


```go
// IndexLookUpJoin employs one outer worker and N innerWorkers to execute concurrently.
// It preserves the order of the outer table and support batch lookup.
//
// The execution flow is very similar to IndexLookUpReader:
// 1. outerWorker read N outer rows, build a task and send it to result channel and inner worker channel.
// 2. The innerWorker receives the task, builds key ranges from outer rows and fetch inner rows, builds inner row hash map.
// 3. main thread receives the task, waits for inner worker finish handling the task.
// 4. main thread join each outer row by look up the inner rows hash map in the task.

type IndexLookUpJoin struct {
	baseExecutor

	resultCh   <-chan *lookUpJoinTask
	cancelFunc context.CancelFunc
	workerWg   *sync.WaitGroup

	outerCtx outerCtx
	innerCtx innerCtx

	task       *lookUpJoinTask
	joinResult *chunk.Chunk
	innerIter  chunk.Iterator

	joiner      joiner
	isOuterJoin bool

	requiredRows int64

	indexRanges   []*ranger.Range
	keyOff2IdxOff []int
	innerPtrBytes [][]byte

	// lastColHelper store the information for last col if there's complicated filter like col > x_col and col < x_col + 100.
	lastColHelper *plannercore.ColWithCmpFuncManager

	memTracker *memory.Tracker // track memory usage.

	stats *indexLookUpJoinRuntimeStats
}
```

实现要点如下：
1. outerWorker 只有一个, 负责从outer executor中读取一个batch数据，建立lookUpJoinTask然后放入innerCh和resultCh中
2. innerCh将由inner worker来consume, 在innser worker处理完这个task之后，才会标记该task为done
3. resultCh 将由executor的Next来consume, executor的Next从resultCh取出一个task之后，会一直等到这个task 为done，然后去做join
这样保证了结果顺序和outer表中顺序一致。
4. inner worker可以有N个，inner worker会去innser表根据index查找在这个batch 范围内的inner executor数据, 最后建立lookupMap, 在executor.Next中match时候会用到该map

![index lookup join](./dot/index_lookup_join.svg)

buildExecutorForIndexJoin

![buildExecutorForIndexJoin](./dot/build_executor_for_index_join.svg)
