# Join算法

<!-- toc -->

## Nest loop join

`nest loop join`, 遍历取外表R中一条记录r, 然后遍历inner表S每条记录和r做join。
对于外表中的每一条记录，都需要对Inner表做一次全表扫描。IO比较高

```
algorithm nested_loop_join is
    for each tuple r in R do
        for each tuple s in S do
            if r and s satisfy the join condition then
                yield tuple <r,s>
```

## Block nest loop join

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

## Indexed Nested loop join

`index join` inner表中对于要join的attribute由了索引, 可以使用索引
来避免对inner表的全表扫描, 复杂度为`O(M * log N)`

```
for each tuple r in R do
    for each tuple s in S in the index lookup do
        yield tuple <r,s>
```

## Hash join

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

## Sort MergeJoin

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

