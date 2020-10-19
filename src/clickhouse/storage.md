# Storage

<!-- toc -->

## IStorage Struct

> Storage. Describes the table. Responsible for
> - storage of the table data;
> - the definition in which files (or not in files) the data is stored;
> - data lookups and appends;
> - data storage structure (compression, etc.)
> - concurrent access to data (locks, etc.)

![istorage struct](./dot/istorage-struct.svg)


```cpp
struct StorageInMemoryMetadata
{
    /// Columns of table with their names, types,
    /// defaults, comments, etc. All table engines have columns.
    ColumnsDescription columns;
    /// Table indices. Currently supported for MergeTree only.
    IndicesDescription secondary_indices;
    /// Table constraints. Currently supported for MergeTree only.
    ConstraintsDescription constraints;
    /// PARTITION BY expression. Currently supported for MergeTree only.
    KeyDescription partition_key;
    /// PRIMARY KEY expression. If absent, than equal to order_by_ast.
    KeyDescription primary_key;
    /// ORDER BY expression. Required field for all MergeTree tables
    /// even in old syntax MergeTree(partition_key, order_by, ...)
    KeyDescription sorting_key;
    /// SAMPLE BY expression. Supported for MergeTree only.
    KeyDescription sampling_key;
    /// Separate ttl expressions for columns
    TTLColumnsDescription column_ttls_by_name;
    /// TTL expressions for table (Move and Rows)
    TTLTableDescription table_ttl;
    /// SETTINGS expression. Supported for MergeTree, Buffer and Kafka.
    ASTPtr settings_changes;
    /// SELECT QUERY. Supported for MaterializedView and View (have to support LiveView).
    SelectQueryDescription select;
    //...
}
```

## IStorage Interface

### watch/read/write

```cpp
    virtual BlockInputStreams watch(
        const Names & /*column_names*/,
        const SelectQueryInfo & /*query_info*/,
        const Context & /*context*/,
        QueryProcessingStage::Enum & /*processed_stage*/,
        size_t /*max_block_size*/,
        unsigned /*num_streams*/)
    {
        throw Exception("Method watch is not supported by storage " + getName(), ErrorCodes::NOT_IMPLEMENTED);
    }

    virtual Pipes read(
        const Names & /*column_names*/,
        const StorageMetadataPtr & /*metadata_snapshot*/,
        const SelectQueryInfo & /*query_info*/,
        const Context & /*context*/,
        QueryProcessingStage::Enum /*processed_stage*/,
        size_t /*max_block_size*/,
        unsigned /*num_streams*/)
    {
        throw Exception("Method read is not supported by storage " + getName(), ErrorCodes::NOT_IMPLEMENTED);
    }

    virtual BlockOutputStreamPtr write(
        const ASTPtr & /*query*/,
        const StorageMetadataPtr & /*metadata_snapshot*/,
        const Context & /*context*/)
    {
        throw Exception("Method write is not supported by storage " + getName(), ErrorCodes::NOT_IMPLEMENTED);
    }

    virtual void drop() {}

    virtual void truncate(
        const ASTPtr & /*query*/,
        const StorageMetadataPtr & /* metadata_snapshot */,
        const Context & /* context */,
        TableExclusiveLockHolder &)
    {
        throw Exception("Truncate is not supported by storage " + getName(), ErrorCodes::NOT_IMPLEMENTED);
    }

```

### rename

```cpp
    virtual void rename(const String & /*new_path_to_table_data*/, const StorageID & new_table_id)
    /**
     * Just updates names of database and table without moving any data on disk
     * Can be called directly only from DatabaseAtomic.
     */
    virtual void renameInMemory(const StorageID & new_table_id);
```

### alter: add/drop columns
```cpp
    /** ALTER tables in the form of column changes that do not affect the change
      * to Storage or its parameters. Executes under alter lock (lockForAlter).
      */
    virtual void alter(const AlterCommands & params, const Context & context, TableLockHolder & alter_lock_holder);

    /** Checks that alter commands can be applied to storage. For example, columns can be modified,
      * or primary key can be changes, etc.
      */
    virtual void checkAlterIsPossible(const AlterCommands & commands, const Settings & settings) const;

    /** ALTER tables with regard to its partitions.
      * Should handle locks for each command on its own.
      */
    virtual void alterPartition(const ASTPtr & /* query */, const StorageMetadataPtr & /* metadata_snapshot */, const PartitionCommands & /* commands */, const Context & /* context */)
    {
        throw Exception("Partition operations are not supported by storage " + getName(), ErrorCodes::NOT_IMPLEMENTED);
    }
```

#### AlterCommands

```cpp
/// Operation from the ALTER query (except for manipulation with PART/PARTITION).
/// Adding Nested columns is not expanded to add individual columns.
struct AlterCommand
{
    /// The AST of the whole command
    ASTPtr ast;

    enum Type
    {
        ADD_COLUMN,
        DROP_COLUMN,
        MODIFY_COLUMN,
        COMMENT_COLUMN,
        MODIFY_ORDER_BY,
        ADD_INDEX,
        DROP_INDEX,
        ADD_CONSTRAINT,
        DROP_CONSTRAINT,
        MODIFY_TTL,
        MODIFY_SETTING,
        MODIFY_QUERY,
        RENAME_COLUMN,
    };
...
```


### mutate
```cpp
    /// Mutate the table contents
    virtual void mutate(const MutationCommands &, const Context &)
    {
        throw Exception("Mutations are not supported by storage " + getName(), ErrorCodes::NOT_IMPLEMENTED);
    }

    /// Cancel a mutation.
    virtual CancellationCode killMutation(const String & /*mutation_id*/)
    {
        throw Exception("Mutations are not supported by storage " + getName(), ErrorCodes::NOT_IMPLEMENTED);
    }
```

#### MutationCommand

```cpp
/// Represents set of actions which should be applied
/// to values from set of columns which statisfy predicate.
struct MutationCommand
{
    ASTPtr ast; /// The AST of the whole command

    enum Type
    {
        EMPTY,     /// Not used.
        DELETE,
        UPDATE,
        MATERIALIZE_INDEX,
        READ_COLUMN,
        DROP_COLUMN,
        DROP_INDEX,
        MATERIALIZE_TTL,
        RENAME_COLUMN,
    };

    Type type = EMPTY;
    ...
}
```

### optimize: backgroud work
```cpp
    /** Perform any background work. For example, combining parts in a MergeTree type table.
      * Returns whether any work has been done.
      */
    virtual bool optimize(
        const ASTPtr & /*query*/,
        const StorageMetadataPtr & /*metadata_snapshot*/,
        const ASTPtr & /*partition*/,
        bool /*final*/,
        bool /*deduplicate*/,
        const Context & /*context*/)
    {
        throw Exception("Method optimize is not supported by storage " + getName(), ErrorCodes::NOT_IMPLEMENTED);
    }
```

### startup/shutdown

```cpp
    /** If the table have to do some complicated work on startup,
      *  that must be postponed after creation of table object
      *  (like launching some background threads),
      *  do it in this method.
      * You should call this method after creation of object.
      * By default, does nothing.
      * Cannot be called simultaneously by multiple threads.
      */
    virtual void startup() {}

    /** If the table have to do some complicated work when destroying an object - do it in advance.
      * For example, if the table contains any threads for background work - ask them to complete and wait for completion.
      * By default, does nothing.
      * Can be called simultaneously from different threads, even after a call to drop().
      */
    virtual void shutdown() {}
```

## Storage Inherit

主要分为StorageLog, MergeTree, SystemData还有类似StorageMySQL等external Data的

![istorage inherit](./dot/istorage-inherit.svg)


### System Storage

system storage 在clickhouse中可以通过use system, 然后 show tables 看到
可以通过表查询clickhouse的各种信息。

```
>use system;
>show tables;
```

```cpp
 aggregate_function_combinators │
│ asynchronous_metrics           │
│ build_options                  │
│ clusters                       │
│ collations                     │
│ columns                        │
│ contributors                   │
│ current_roles                  │
│ data_type_families             │
│ databases                      │
│ detached_parts                 │
│ dictionaries                   │
│ disks                          │
│ distribution_queue             │
│ enabled_roles                  │
│ events                         │
│ formats                        │
│ functions                      │
│ grants                         │
│ graphite_retentions            │
│ licenses                       │
│ macros                         │
│ merge_tree_settings            │
│ merges                         │
│ metric_log                     │
│ metric_log_0                   │
│ metrics                        │
│ models                         │
│ mutations                      │
│ numbers                        │
│ numbers_mt                     │
│ one                            │
│ parts                          │
│ parts_columns                  │
│ privileges                     │
│ processes                      │
│ query_log                      │
│ query_thread_log               │
│ quota_limits                   │
│ quota_usage                    │
│ quotas                         │
│ quotas_usage                   │
│ replicas                       │
│ replication_queue              │
│ role_grants                    │
│ roles                          │
│ row_policies                   │
│ settings                       │
│ settings_profile_elements      │
│ settings_profiles              │
│ stack_trace                    │
│ storage_policies               │
│ table_engines                  │
│ table_functions                │
│ tables                         │
│ trace_log                      │
│ trace_log_0                    │
│ users                          │
│ zeros                          │
│ zeros_mt                       │
└────────────
```


### MergeTreeData

### StorageLog
