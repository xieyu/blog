# 基本概念 

<!-- toc -->


在 TiDB 中，我们维护的统计信息包括表的总行数，列的等深直方图，Count-Min Sketch，Null 值的个数，平均长度，不同值的数目等等
用于快速估算代价。

## 等深直方图

相比于等宽直方图，等深直方图在最坏情况下也可以很好的保证误差
等深直方图，就是落入每个桶里的值数量尽量相等。

## CMSketch

Count-Min Sketch 是一种可以处理等值查询，Join 大小估计等的数据结构，并且可以提供很强的准确性保证。自 2003 年在文献 An improved data stream summary: The count-min sketch and its applications 中提出以来，由于其创建和使用的简单性获得了广泛的使用。

## FMSketch

