# RangesScanner

提供了统一的next接口，从Storage中遍历多个Key Range

![](./dot/ranges_scanner.svg)


## TiKVStorage

![](./dot/TiKVStorage.svg)


## Snapshot

```rust
/// A Snapshot is a consistent view of the underlying engine at a given point in time.
///
/// Note that this is not an MVCC snapshot, that is a higher level abstraction of a view of TiKV
/// at a specific timestamp. This snapshot is lower-level, a view of the underlying storage.
pub trait Snapshot: Sync + Send + Clone {
    type Iter: Iterator;

    /// Get the value associated with `key` in default column family
    fn get(&self, key: &Key) -> Result<Option<Value>>;

    /// Get the value associated with `key` in `cf` column family
    fn get_cf(&self, cf: CfName, key: &Key) -> Result<Option<Value>>;

    /// Get the value associated with `key` in `cf` column family, with Options in `opts`
    fn get_cf_opt(&self, opts: ReadOptions, cf: CfName, key: &Key) -> Result<Option<Value>>;
    fn iter(&self, iter_opt: IterOptions) -> Result<Self::Iter>;
    fn iter_cf(&self, cf: CfName, iter_opt: IterOptions) -> Result<Self::Iter>;
    // The minimum key this snapshot can retrieve.
    #[inline]
    fn lower_bound(&self) -> Option<&[u8]> {
        None
    }
    // The maximum key can be fetched from the snapshot should less than the upper bound.
    #[inline]
    fn upper_bound(&self) -> Option<&[u8]> {
        None
    }

    /// Retrieves a version that represents the modification status of the underlying data.
    /// Version should be changed when underlying data is changed.
    ///
    /// If the engine does not support data version, then `None` is returned.
    #[inline]
    fn get_data_version(&self) -> Option<u64> {
        None
    }

    fn is_max_ts_synced(&self) -> bool {
        // If the snapshot does not come from a multi-raft engine, max ts
        // needn't be updated.
        true
    }
}
```

![](./dot/range_scanner_snapshot.svg)

调用RaftEngine的`async_snapshot`获取snapshot

![](./dot/range_scanner_snaphost_from.svg)

## tls engine

![](./dot/range_scanner_tls_engine.svg)
