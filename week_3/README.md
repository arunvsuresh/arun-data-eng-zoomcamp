Data Warehouse & BigQuery
*  OLAP vs OLTP
    * OLTP (online transaction processing)
        * Backend services
        * Group couple of sql queries together
        * Rollback in case one of them fails 
        * Fast but small updates 
        * Normalized data 
        * Increases productivity for end users
        * Use case: Customer facing personnel, clerks, online shoppers
    * OLAP (online analytical processing)
        * More used for putting lot of data in and discovering hidden insights
        * Analytical purposes used by analysts/data scientists
        * Data is periodically refreshed
        * Data size is far larger 
        * Denormalized data
        * Increases productivity for analysts/execs
        * Use case: knowledge workers such as data analysts, execs
* What is a Data Warehouse?
    * OLAP solution used for data reporting and analysis
    * Consists of raw data, metadata, summary
    * Data sources: operational system, flat files, etc.
    * Put into staging area from data source
    * From staging put into warehouse then put into data marts
* BigQuery
    * Serverless data warehouse
        * No servers to manage or database software to install
    * Provides software as well as infra for scalialbity and availability 
    * Built-in features
        * Machine learning via sql interface
        * Geo-spatial data
        * BI queries
    * Maximizes flexibility by separating compute engine that analyzes your data from your storage
    * Bigquery general caches data
    * Cost
        * On demand pricing
            * Based on amount of data processed
        * Flat rate pricing
            * Based on no. of pre-requested slots
    * Partitioning in BigQuery
        * Data is partitioned by some field or row value, e.g. date
        * Once BigQuery understands that it only needs to get data for certain partition, will not process other partitions, which reduces costs b/c it’s processing less data
    * Clustering in BigQuery
        * Can add additional field to “cluster” data in addition to partitioning to help organize and improve query performance and decrease costs
    * Partitioning vs Clustering in detail
        * Partition
            * Can choose between following partitions:
                * Time-unit column
                * Ingestion time (_PARTITIONTIME)
                * Integer range partitioning
            * When using time unit or ingestion time
                * Daily(default)
                * hourly
                * Monthly or yearly
            * No. Of partitions limit is 4000
        * Clustering
            * Columns you specific to cluster are used to colocate related data
            * Order of column is important
            * Order of specified columns determines sort order  of the data
            * Clustering improves
                * Filter queries
                * Aggregate queries
            * Table with table size < 1GB don’t show improvement with partitioning & clustering
                * B/c partitioning and clustering incur costs with metadata reads & metadata maintenance
            * You can specificy up to 4 clustering columns
            * Columns must be top-level, non-repeated columns
        * Comparison
            * Clustering
                * Cost benefit unknown
                * Better when Need more granularity
                * Queries commonly use filters or aggregation against multiple particular columns 
                * Cardinality of no. of values in a column or group of columns is large
            * Partitioning 
                * Cost known upfront
                * Better for partition-level management
                * Filter or aggregate on single column
        * When to choose clustering over partitioning?
            * Parititinog results in small amount of data per partition (approx less than 1 GB)
            * Partitioning results in large no. of partitions bond the limits on partitioned tables
            * Partitioning results in mutation operations modifying majority of partitions in table frequently (for example every few minutes)
        * Automatic Clustering
            * As data is added to a clustered table
                * the newly inserted data can be written to blocks that contain key ranges that overlap with the key ranges in previously written blocks
                * These overlapping keys weaken the sort property of the table
            * To maintain the performance characteristics of a clustered table
                * BigQuery performs automatic re-clustering in background to restore sort property of table
                * For partitioned tables, clustering is maintained for data within the scope of each partition.
    * BigQuery best practices
        * Cost reduction
            * Always avoid select *, BigQuery stores data in columnar storage
            * Price your queries before running them (can be seen on top right corner)
            * Use clustered or partitioned tables
            * Use streaming inserts with caution
                * Can increase costs drastically
            * Materialize query results in stages
        * Query performance
            * Filter on partitioned columns
            * Denormalize data
            * Use nested or repeated columns
            * Use external data sources appropriately 
                * Should not do it too much, b/c while reading from gcs, might incur more cost
            * Reduce data before using join
            * Do not treat with clauses as prepared statements
            * Avoid oversharding tables
    * Internals of BigQuery
        * Stores data into separate storage called Colossus
            * Colossus - cheap storage which stores data in columnar format
            * Big advantage - storage separated from compute, has much less cost, storage and compute on separate hardware
        * Most cost incurred during compute
        * How do storage and compute communicate with each other?
            * Jupiter network
                * Inside bigquery datacenters
                * Provides 1TB per second network speed
        * Dremel
            * Query execution engine
                * Divides query into tree structure
            * Separates query in such a way that each node can execute individual subset of query
        * Internals of record-oriented vs column-oriented storage
            * BigQuery uses column oriented structure
                * Provide huge gain
                * Better aggregation on columns
                * Generally we do not query all columns at one time, query few columns and filter and aggregate on different ones
        * Internals of Dremel
            * When bigQuery root server receives query, it understands know how to divide into smaller sub-modules and propagate them to leaf nodes
* ML in BigQuery