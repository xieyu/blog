# ProgressTracker

![](./dot/raft_progresstracker.svg)

## progress tracker初始化

## maximal committed index

计算committed index

```rust
/// Returns the maximal committed index for the cluster. The bool flag indicates whether
/// the index is computed by group commit algorithm successfully.
///
/// Eg. If the matched indexes are [2,2,2,4,5], it will return 2.
/// If the matched indexes and groups are `[(1, 1), (2, 2), (3, 2)]`, it will return 1.
pub fn maximal_committed_index(&mut self) -> (u64, bool)
```

## tally votes

统计election 投票
