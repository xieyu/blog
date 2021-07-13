# Selection

调用Src BatchExecutor的next_batch, 获取数据，然后对于自己的每个condition
调用 RpnExpression::eval, 计算condition的结果，然后只保留condition为true的
logical rows.


![](./dot/batch_executor_selection.svg)

### next_batch

这里面RpnExpression是逆波兰表达式，比如2 *（3 + 4）+ 5 会被
表示为: 2 3 4 + * 5 +。


![](./dot/batch_executor_selection_next_batch.svg)

RpnExpression eval时，从左到右遍历表达式，遇到操作数(比如数字2,3)，
就push到stack中，遇到operator(比如+号)就从Stack中pop出operator需要的参数
比如+就pop 3和4，然后将 3 4 +的执结果7push到stack中。最后stack中就是执行的结果。

对应的执行逻辑在代码`RpnExpression::eval_decoded`函数中

```rust
    pub fn eval_decoded<'a>(
        &'a self,
        ctx: &mut EvalContext,
        schema: &'a [FieldType],
        input_physical_columns: &'a LazyBatchColumnVec,
        input_logical_rows: &'a [usize],
        output_rows: usize,
    ) -> Result<RpnStackNode<'a>> {

```

