# Compaction Picker

## level compaction picker

以下两张图摘自facebook wiki [leveled-compaction](https://github.com/facebook/rocksdb/wiki/Leveled-Compaction)

![level 0 compaction ](./pre_l0_compaction.png)

![level 1 compaction](./pre_l1_compaction.png)

### compaction picker调用关系

![level-compaction-picker](./level-compaction-picker.svg)

## Ref
1. leveled-compaction: https://github.com/facebook/rocksdb/wiki/Leveled-Compaction
