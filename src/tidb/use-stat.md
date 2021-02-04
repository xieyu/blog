# 统计信息使用场景

<!-- toc -->

## 加载统计信息
从mysql.stats_*表中加载信息。

每个TiDB server有个goroutine 周期性的更新stat信息
Handle can update stats info periodically.


在TiDB启动时候，会启动一个goroutine, loadStatsWorker

![](./dot/loadStatsWorker.svg)

Update, 更新statsCache

![](./dot/stat_handle.svg)

加载载table的Histogram和CMSketch tableStatsFromStorage

![](./dot/tableStatsFromStorage.svg)


## Selectivity

### StatsNode
```go
// StatsNode is used for calculating selectivity.
type StatsNode struct {
	Tp int
	ID int64
	// mask is a bit pattern whose ith bit will indicate whether the ith expression is covered by this index/column.
	mask int64
	// Ranges contains all the Ranges we got.
	Ranges []*ranger.Range
	// Selectivity indicates the Selectivity of this column/index.
	Selectivity float64
	// numCols is the number of columns contained in the index or column(which is always 1).
	numCols int
	// partCover indicates whether the bit in the mask is for a full cover or partial cover. It is only true
	// when the condition is a DNF expression on index, and the expression is not totally extracted as access condition.
	partCover bool
}
```

```go
// Selectivity is a function calculate the selectivity of the expressions.
// The definition of selectivity is (row count after filter / row count before filter).
// And exprs must be CNF now, in other words, `exprs[0] and exprs[1] and ... and exprs[len - 1]` should be held when you call this.
// Currently the time complexity is o(n^2).
```

Selectivity: 
1. 计算表达式的ranges: ExtractColumnsFromExpressions

questions:
1. correlated column 是什么意思？
2. maskCovered作用是什么
3. statsNode的作用是什么

![](./dot/selectivity.svg)

## 参考

1. [TiDB 源码阅读系列文章（十二）统计信息(上)](https://pingcap.com/blog-cn/tidb-source-code-reading-12/)
2. [TiDB 源码阅读系列文章（十四）统计信息（下)](https://pingcap.com/blog-cn/tidb-source-code-reading-14/)
3. [TiDB统计信息原理简介与实践](https://asktug.com/t/topic/37691)
