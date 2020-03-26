# Compact

### PickCompaction

选择要合并compact的FileMetaData

![pick-compaction](./pick-compaction.svg)

### 多路归并Compact

将选择好的FilemetaData合并，输出到level+1层。通过versionEdit更改Version.

![db-compact](./do-compaction.svg)
