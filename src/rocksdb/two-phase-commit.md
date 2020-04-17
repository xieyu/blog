# Two phase commit

### Write Commited txn

事务只有在提交之后，写到DB中,

![write commited](./write-committed.svg)

WriteCommited 两阶段提交：

* Prepare阶段 将writebatch 写入WAL日志中,并将writeBatch中内容用`ktypeBeginPrepare(Xid)`, `kTypeEndPrepare(xid)` 括起来
由于只写到了WAL日志中,　其他事务看不到这个事务的修改
* Commit阶段 向WAL日志写入commit 标记，比如`kTypeCommit(xid)` 并writeBatch中内容insert到memtable上，写入memtable之后，该事务的修改对其他事务就可以见了。


![two-phase-commit-write-batch](./two-phase-commit-write-batch.svg)

```cpp
Status WriteBatchInternal::MarkEndPrepare(WriteBatch* b, const Slice& xid,
                                          bool write_after_commit,
                                          bool unprepared_batch) {
  // other code..
  // rewrite noop as begin marker
  b->rep_[12] = static_cast<char>(
      write_after_commit ? kTypeBeginPrepareXID
                         : (unprepared_batch ? kTypeBeginUnprepareXID
                                             : kTypeBeginPersistedPrepareXID));
  b->rep_.push_back(static_cast<char>(kTypeEndPrepareXID));
  PutLengthPrefixedSlice(&b->rep_, xid);
  // other code..
}
```


### Write prepared txn

![write unprepared](./two-phase-commit-write-preparedtxn.svg)

## Recover

![two phase commit recover](./two-phase-commit-recover.svg)
