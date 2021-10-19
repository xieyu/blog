# SkipList

## SkipList 算法

SkipList是William Pugh 在 1990论文：Skip Lists: A Probabilistic Alternative to Balanced Trees
中提出的一个数据结构。

最低层level 0的为全链表，level 1层为level 0层的一半，level i层node个数为level (i-1)层的一半，越往上越稀疏。

![](./dot/Linked_lists_with_additional_pointers.png)

插入和查询

![](./dot/skiplist_insert.png)


## data struct

![](./dot/skiplist.svg)


## insert
