# Analyze

<!-- toc -->

## AnalyzeExec

在执行 analyze 语句的时候，TiDB 会将 analyze 请求下推到每一个 Region 上，然后将每一个 Region 的结果合并起来。

Analyze 语句

![](./dot/AnalyzeExec.svg)

## analyzeColumnsPushdown

![](./dot/analyzeColumnsPushdown.svg)

## analyzeIndexPushdown

![](./dot/analyzeIndexPushdown.svg)
