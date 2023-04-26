Analytics Engineering
*  What is analytics engineering?
    * Introduces good software eng practices to efforts of data analysts and data scientists 
    * tools
        * Data loading (fivetran, stitch)
        * Data storing (cloud data warehouse)
        * Data modeling (dbt)
        * Data presentation (google data studio, looker)
* Data modeling concepts
    * ETL vs ELT
        * ETL
            * Extract sources, transform, load to DWH
            * Takes longer to implement b/c first have to transform data, but data is cleaner
        * ELT
            * Transform data once inside DWH
            * Faster and more flexible b/c data is already loaded
* Kimball’s dim modeling
    * objective
        * Deliver data that’s understandable to biz user
        * Deliver fast query performance
    * approach
        * Prioritize user understandability and query performance over non redundant data (3NF)
    * Other approaches
        * Bill inmon
        * Data vault
* Elements of dim modeling (star schema)
    * Fact tables
        * Measurements, metrics, or facts about biz
        * Corresponds to a biz process
        * “Verbs”, e.g. sales or orders
    * Dim tables
        * Provide context to fact tables
        * Correspond to biz identity
        * Provides context to biz process
        * “Nouns”, e.g. customer or product
    * Architecture of dim modeling
        * Stage area
            * Contains raw data
            * Not meant to be exposed to everyone, only to people who know how to use that raw data
        * Processing area
            * From raw data to data models, again limited to those who know how to take raw data to data models
            * Focuses on efficiency
            * Ensuring standards
        * Presentation area
            * Final presentation of data
            * Exposure to biz stakeholder

DBT
* Data build tool
    * dbt is a transformation tool that allows anyone that knows SQL to deploy analytics code following software engineering best practices like modularity, portability, CI/CD, and documentation.
    * Going to help with transformation of data
    * After extraction and loading, have lot of raw data in DWH, need to transform that data
* How does dbt work?
    * Add modeling layer where we are going to transform the data
    * This model with the transformed data is being persisted back to the data warehouse
    * We write sql files (dbt models)
        * Essentially select statements
        * Dbt compiles that file
            * Creates a ddl or dml file then it’s going to push that compute to our DWH
            * At the end we are going to be able to see that table or view in the warehouse
* How to use dbt?
    * Dbt core
        * Open-source project that allows the data transformation
            * Builds and runs a dbt project (.sql and .yml files)
            * Includes sql compilation logic, macros, and database adapters
            * Includes cli interface to run dbt commands locally
    * Dbt cloud
        * SaaS application to develop and manage dbt projects 
        * Web-based IDE to develop, run, and test dbt project 
        * Job orchestration
        * Logging & alerting
        * Integrated docs
* Build the first dbt Models
    * Models have Curly braces
        * We can write in jinja (we can use functions/macros to help us generate full code when dbt model compiles)
        * e.g. {{config(materialized=’table’)}} — add DDL or DML to model we are writing
    * Materialization strategies (how to create particular data schema for use) 
        * table
        * view
        * incremental
        * ephemeral
    * Dbt model file goes from something like this:
        {{config(materialized=’table’)}}
        Select * from staging.source_table where  
record_state = ‘ACTIVE’
   to…
    Create table my_schema.my_model as (
        Select * from staging.source_table where record_state = 'ACTIVE’)
        * Dbt runs compiled code in data warehouse, e.g. bigquery
    * FROM clause of dbt model
        * Sources 
            * The data loaded to our dwh that we use as sources for our models
            * Configuration defined in the yml files in the models folder
            * Used with the source macro that will resolve the name to the right schema, plus build the dependencies automatically 
            * Source freshness can be defined and
        * Seeds, or loading from CSV files
            * CSV files stored in our repo under seed folder
            * Benefits of version controlling
            * Equivalent to a copy command
            * Recommended for data that doesn’t change frequently 
            * Runs with dbt seed -s file_name
        * Ref
            * Macro that allows us to reference underlying tables and views that we have in DWH
            * Run the same code in any environment, it will resolve the correct schema for you
            * Dependencies are built automatically
    * Macros
        * Similar to functions, we write macros using jinja templating syntax
        * Return code 
        * We create a separate file within a macros folder
        * Use control structures (e.g. if statements and for loops) in SQL 
        * Use environment variables in your dbt project for production  deployments 
        * Operate on the results of one query to generate another query 
        * Abstract snippets of SQL into reusable macros — these are  analogous to functions in most programming languages.
    * Packages
        * Dbt projects that have models and macros of their own, also test…can import to your own project
        * Like libraries in other programming languages
        * Standalone dbt projects, with models and macros that tackle a specific problem area.
        * By adding a package to your project, the package's models and macros will become part of your own project.
        * Imported in the packages.yml file and imported by running dbt deps
        * A list of useful packages can be find in dbt package hub
    * Variables
        * Variables are useful for defining values that should be used across the project
        * With a macro, dbt allows us to provide data to models for compilation
        * To use a variable we use the {{ var('...') }} function
        * Variables can defined in two ways:
            * In the dbt_project.yml file
            * On the command line
    * Seeds
        * CSV files that we can have in our repo and run and use as tables with the right macro 
        * Meant to be used for smaller files that have data that doesn’t change that often
        * If working in the cloud, can commit, push, and if file in remote repo, can pull so it appears in dbt cloud
        * dbt seed
            * Creates table in db
            * Will automatically resolve data types
        * dbt seed --full-refresh
            * Enforce that it drops the table and re-create with new values (if new values added to file)
    * Note:
        * dbt run only will run models, not seeds
        * dbt build runs seeds, models, and tests
        * dbt build --select fact_trips — will only run the fact_trips model, but dbt build --select +fact_trips — will run fact_trips and everything else it depends on/needs (builds upstream)
            * Dbt resolves models for us and runs models in order they need to be according to those dependencies
            * dbt build does dbt run + dbt test behind the scenes for each component in the DAG
        * dbt test —select <model_name>
            * Will run tests from the specified model
            * Tests are configured to run set of error rows
        * dbt test —select source:<source_name>
            * Will run tests on source, specified either through .yml file or distinct test file within /tests folder
* Testing and Documenting the Project
    * Deployment of dbt project
        * yml file overview
            * In .yml file Mandatory part that we always have to add are the sources, otherwise dbt will not know how to resolve location of those sources
            * Can also add another section for our models
    * documentation
        * Doc blocks
            * Live in a markdown file
* Deployment of dbt project
    * Dev workflow
        * development environment
            * Normally in a a separate branch
            * Testing and documenting models
            * Has own separate schema and it will be a  separate user ideally
        * Once ready, we deploy using version control and CI/CD in a production environment
