# Versionset和Manifest

## Manifest文件写入

version记录了当前每个level的各个文件的FileMetadata.

在压缩时候，每个level的FileMetadata可能会更改, 这种修改是用VersionEdit来表示的, 每次修改会将VersionEdit Encode写入日志中, 方便崩溃时候能够从Manifest日志文件中恢复。

![versionset](./versionset-edit.svg)

## Recover

Current文件内容记录了当前的manifest文件, 在DBOpen时候会去加载Mainfest文件，然后读取每个versionEditRecord
将它Decode为VersionEdit，然后一个个的apply，最终得到最后的version, 最后加入到VersionSet中。

![versionset](./versionset-recover.svg)


遗留问题：
SequenceNumber和FilNumber这些是怎么保存的？
