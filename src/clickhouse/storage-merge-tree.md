# StorageMergeTree

<!-- toc -->

什么是MergeTree？原理是啥？有啥优缺点

> MergeTree存储结构需要对用户写入的数据做排序然后进行有序存储，数据有序存储带来两大核心优势：

## struct

## read

![storage-merge-tree-read](./dot/storage-merge-tree-read.svg)

## write

write 返回一个`MergeTreeBlockOutputStream`

![storage merge tree write](./dot/storage-merge-tree-write.svg)

### WriteTempPart

![write tmp](./dot/merge-tree-data-writer-writeTmp.svg)

## mutate

![storage-merge-tree-mutate](./dot/storage-merge-tree-mutate.svg)

## mergeMutateTask

![mergeMuteTask](./dot/merge-mute-task.svg)

### finalizeMutatedPart

Initialize and write to disk new part fields like checksums, columns,
