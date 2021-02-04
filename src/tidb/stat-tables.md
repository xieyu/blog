# stats tables

<!-- toc -->

## 统计信息存储

在TiDB中统计信息会存在几个表中

* `mysql.stats_meta`: 统计信息元信息
* `mysql.stats_histograms`: 统计信息直方图
* `mysql.stats_buckets` : 统计信息桶
* `mysql.stats_extended`
* `mysql.stats_feedback` : 收集的stats feedback， 会被定期apply到上面的表中


```sql
	// CreateStatsMetaTable stores the meta of table statistics.
	CreateStatsMetaTable = `CREATE TABLE IF NOT EXISTS mysql.stats_meta (
		version 		BIGINT(64) UNSIGNED NOT NULL,
		table_id 		BIGINT(64) NOT NULL,
		modify_count	BIGINT(64) NOT NULL DEFAULT 0,
		count 			BIGINT(64) UNSIGNED NOT NULL DEFAULT 0,
		INDEX idx_ver(version),
		UNIQUE INDEX tbl(table_id)
	);`

	// CreateStatsColsTable stores the statistics of table columns.
	CreateStatsColsTable = `CREATE TABLE IF NOT EXISTS mysql.stats_histograms (
		table_id 			BIGINT(64) NOT NULL,
		is_index 			TINYINT(2) NOT NULL,
		hist_id 			BIGINT(64) NOT NULL,
		distinct_count 		BIGINT(64) NOT NULL,
		null_count 			BIGINT(64) NOT NULL DEFAULT 0,
		tot_col_size 		BIGINT(64) NOT NULL DEFAULT 0,
		modify_count 		BIGINT(64) NOT NULL DEFAULT 0,
		version 			BIGINT(64) UNSIGNED NOT NULL DEFAULT 0,
		cm_sketch 			BLOB,
		stats_ver 			BIGINT(64) NOT NULL DEFAULT 0,
		flag 				BIGINT(64) NOT NULL DEFAULT 0,
		correlation 		DOUBLE NOT NULL DEFAULT 0,
		last_analyze_pos 	BLOB DEFAULT NULL,
		UNIQUE INDEX tbl(table_id, is_index, hist_id)
	);`

	// CreateStatsBucketsTable stores the histogram info for every table columns.
	CreateStatsBucketsTable = `CREATE TABLE IF NOT EXISTS mysql.stats_buckets (
		table_id 	BIGINT(64) NOT NULL,
		is_index 	TINYINT(2) NOT NULL,
		hist_id 	BIGINT(64) NOT NULL,
		bucket_id 	BIGINT(64) NOT NULL,
		count 		BIGINT(64) NOT NULL,
		repeats 	BIGINT(64) NOT NULL,
		upper_bound BLOB NOT NULL,
		lower_bound BLOB ,
		UNIQUE INDEX tbl(table_id, is_index, hist_id, bucket_id)
	);`

	// CreateStatsFeedbackTable stores the feedback info which is used to update stats.
	CreateStatsFeedbackTable = `CREATE TABLE IF NOT EXISTS mysql.stats_feedback (
		table_id 	BIGINT(64) NOT NULL,
		is_index 	TINYINT(2) NOT NULL,
		hist_id 	BIGINT(64) NOT NULL,
		feedback 	BLOB NOT NULL,
		INDEX hist(table_id, is_index, hist_id)

	// CreateStatsExtended stores the registered extended statistics.
	CreateStatsExtended = `CREATE TABLE IF NOT EXISTS mysql.stats_extended (
		stats_name varchar(32) NOT NULL,
		db varchar(32) NOT NULL,
		type tinyint(4) NOT NULL,
		table_id bigint(64) NOT NULL,
		column_ids varchar(32) NOT NULL,
		scalar_stats double DEFAULT NULL,
		blob_stats blob DEFAULT NULL,
		version bigint(64) unsigned NOT NULL,
		status tinyint(4) NOT NULL,
		PRIMARY KEY(stats_name, db),
		KEY idx_1 (table_id, status, version),
		KEY idx_2 (status, version)
	);`

	// CreateStatsTopNTable stores topn data of a cmsketch with top n.
	CreateStatsTopNTable = `CREATE TABLE IF NOT EXISTS mysql.stats_top_n (
		table_id 	BIGINT(64) NOT NULL,
		is_index 	TINYINT(2) NOT NULL,
		hist_id 	BIGINT(64) NOT NULL,
		value 		LONGBLOB,
		count 		BIGINT(64) UNSIGNED NOT NULL,
		INDEX tbl(table_id, is_index, hist_id)
	);`
```

## 创建 stat tables

这些SQL将由ddl worker owner在启动的时候执行, 创建相应的Table

![](./dot/ddl_worker_create_tables.svg)

## 更新/缓存/加载 stats table

每个TiDB启动后，会调用UpdateTableStatsLoop，分别使用一个goroutine执行如下任务:

1. `autoAnalzeWorker` 定时触发autoAnaly worker, 根据一定规则触发执行`analyze table xxx`, 执行AnlyzeExec,会后将结果写入`mysql.stats_*`中。
2. `loadStatsWorker` 把`mysql.stat_*`信息定期加载到本地缓存中。
3. `updateStatsWorker` 将本地收集的feedback apply到自己的本地缓存上，并写入`mysql.stats_feedback`中，如果该节点是owner, 会将`mysql.stats_feedback`表中信息apply到 `mysql.stat_*`表中。

![](./dot/crud_mysql_stats.svg)
