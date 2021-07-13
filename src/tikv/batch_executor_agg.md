# Agg executor

![](./dot/batch_executor_agg.svg)

## next_batch

![](./dot/Aggregator_next_batch.svg)

## AggregationExecutorImpl

对应四种实现，每个里面都有个states 是`Vec<Box<dyn AggrFunctionState>>`
用来保存aggr state (比如avg 的state需要保存sum和count).

![](./dot/agg_impl.svg)

`SimpleAggregationImpl` 是没有group by 的，比如下面这种SQL。
```sql
select count(*) from table
```

## SimpleAggregationImpl

这个没有groupby

![](./dot/simple_agg_impl.svg)

## FastHashAggregationImpl

这个只有一个group by expr

![](./dot/fast_hash_aggr.svg)

## SlowHashAggregationImpl
有多个group by expr

![](./dot/slow_hash_agg.svg)


假设数据有四列`a`,`b`,`c`,`d`, 执行

```sql
select 
  exp_1(a), exp_2(b), avg(c), sum(d) 
from t 
group by 
  exp_1(a), exp_2(b)
```
slow hash agg中相关数据结构关系如下:

![](./dot/slow_hash_map.svg)

## BatchStreamAggregationImpl

假定已排好序

![](./dot/stream_agg_impl.svg)

stream agg中相关数据结构关系如下:

![](./dot/stream_agg_struct_relationship.svg)
