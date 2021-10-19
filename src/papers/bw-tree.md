# Bw-tree

the Bw-tree achieves its very high performance via a latch-free approach 
that effectively exploits the processor caches of modern multi-core chips.

is paper is on the main memory aspects of the Bw-tree. We describe the details of our latch-free tech- nique,

we need to get better at exploiting a large number of cores by addressing at least two important aspects

1. Multi-core cpus mandate high concurrency. But, as the level of concurrency increases, latches are more likely to block, limiting scalability

lock 限制了多核并发能力

2. Good multi-core processor performance depends on high CPU cache hit ratios. Updating memory in place results in cache invalidations, so how and when updates are done needs great care. 

cpu cache hit rate, 如何利用cpu cache hit rate

the Bw-tree performs “delta” updates that avoid updating a page in place, hence preserving previously cached lines of pages
