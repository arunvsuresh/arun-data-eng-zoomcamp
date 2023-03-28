Data Lake
* What is a data lake?
    *  Central repo that holds big data from many sources
        * Data can be structured, semi-structured, or unstrucutred
    * Idea is to ingest data as quickly as possible and make available as quickly as possible to other team members, e.g. data scientists, analysts, etc.
    * When storing into data lake, associate some metadata for faster access
    * Data lake solution generally has to be secure and scalable
    * Hardware should also be inexpensive 
        * Want to store as much of data as quickly as possible
* Data lake vs data warehouse
    * Data lake
        * Data lake is more unstructured
        * Stores huge amounts of data, e.g petabytes, terabytes
        * Use cases: stream processing, machine learning, real-time analytics
    * Data warehouse
        * Data is generally structured
        * Users are generally business analysts, data size is smaller
        * Use cases: batch processing or bi reporting
* How did idea of data lake come to be?
    * Companies realized value of data
    * Need of storing and accessing data quickly
        * Can’t always wait for data to be defined and structured the right way before accessing it
    * Data is not really useful when project starts but later in lifecycle
        * Important to store data as quickly as possible 
    * Need for cheap storage of big data
* ETL vs ELT
    * Export, transform, load vs export load, transform
    * Etl used for small amount of data, vs elt is used for large amounts of data
    * ETL is data warehouse solution vs ELT is data lake solution
    * Idea of ETL is schema on write - define well defined schema, define relationships and then write data
    * ELT is based on upon schema on read - write data first then determine schema on read
*  Gotchas of Data Lake
    * No versioning
    * Incompatible schemas for same data without versioning
    * No metadata associated
    * Joins not possible
*  Cloud provider for data lake
    * GCP - cloud storage
    * AWS - S3
    * Azure - Azure Blob

Intro to workflow orchestration
*  What is workflow orchestration
    * Means Governing data flow in a way that respects orcheatitonn rules and biz logic
    * What is Data flow?
        * Binds disparate set of applications together
    * Allows you to turn any code into workflow that you can schedule, run, observe
    * Takes care of delivery
        * Means execution of workflow run
    * All about data flow
        * Ensures you can rely on execution by giving you visibility into how long delivery took providing you shipment updates, lets you know if it was successfully shipped
* Core features of workflow orch
    * Remote execution
    * scheduling
    * retries
    * caching
    * integration with external systems (API's, databases)
    * ad-hoc runs
    * parameterization
    * Alerting you when something fails

Prefect concepts
*  benefit of a scheduler
    * Orchestrate job, gain visibility & resilience into when job potentially breaks
* Prefect flow
    * Most basic python object
    * Container of workflow logic that allows to interact and understand state of workflow
    * Much like functions - take inputs, perform work, return outputs
    * Flows can contain tasks
    * Initialize via a decorator
    * Flows can also contain other flows
* Prefect tasks
    * Can receive metadata about upstream dependencies and state of dependencies before function is run
    * Gives opp to have task wait on completion of another task before executing
    * Initialize via a decorator
    * can add automatic retries in case there is some bottleneck/failure upstream, e.g. issue pulling data from data source
    * can add caching layer to task decorator to increase speed/effiency. if previous iteration of task was successful, successive iterations of tasks can pull from cached results to increase task speed.
* Can add parameterization to tasks and flows, increase modularity and DRY-ness
* Prefect Orion
    * UI to see flows
* Prefect blocks
    * Way to store creds and config info to connect to external systems…e.g. Postgres user/password info
    * Create a block in the Orion UI under the blocks tab
    * Select the driver, e.g. postgresql+psycopg2 and enter creds
    * Below Loads sqlalchemyconnector and connects to Postgres db 
        * connection_block = SqlAlchemyConnector.load("postgres-connector") with connection_block.get_connection(begin=False) as engine:

ETL with GCP & Prefect
*  Check etc_web_gcs file 
* Want to make sure we have google cloud blocks ready for us
    * Register gcp blocks from prefect gcp module:
        * “prefect block register -m prefect_gcp"

From GCS to Big Query
 * more on this!

Parametrizing Flow & Deployments with ETL into GCS flow
*  benefits
    * Allowing flow to take parameters so when we schueld flow, it’s not hard-coded, we can pass params at run-time
    * Flow can have multiple flow-runs with diff params that affect how output of file ends up being
* Prefect deployments
    * Trigger and schedule flow runs and not have to do it manually
    * Server-side concept that encapsulates a flow allowing it to be scheduled and triggered via api
    * Start by building a deployment:
        * prefect deployment build <file_name>:<entry_point_to_flow> -n “<name of deployment>"
        * This creates a places an ETL yaml file in dir
            * Metadata that orchestration tool needs to know
    * Then apply deployment to send yaml file metadata to prefect api so it now knows we are scheduling/orchestrating a flow
        * prefect deployment apply <yaml_file>
    * Once built and applied, can run flow from UI
* agent
    * Python process that’s living in execution env
    * Pulling from a work queue
    * Deployment specifies where we want flow to run by sending it to a work queue
    * To execute flow runs from a specific deployment, we start an agent that pull from work queue:
        * Prefect agent start —work-queue “<name of work queue>"


Schedules & Docker Storage with Infrastructure
* after deployment has successfully run, can schedule future runs in Orion UI or through command line:
    * prefect deployment build parameterized_flow.py:etl_parent_flow -n etl2 --cron "0 0 * * *" -a
        * -n — name of deployment build, 
        * —cron — type of scheduler
        * -a — apply build
* Can put our flow code storage in various places - Github, AWS, BitBucket
    * But we’re gonna put it in a docker container
* First we’ll build the image:
    * docker image build -t arunvsuresh/prefect:zoomcamp .
    * Dockerfile contains packages to install and copies directories containing flow code into curr dir for docker image
* Next push image to dockerhub:
    * docker image push arunvsuresh/prefect:zoomcamp
* Make docker block in prefect Orion UI to be able to register docker container env vars/creds via Prefect
    * 
* Prefect deployment from python script
    * Refer to docker_deploy.py
* Start prefect agent: prefect agent start -q default
    * Look for work from default work queue
* Run flow via deployment command:
    * prefect deployment run etl-parent-flow/docker-flow -p "months=[1, 2]"
    * ^above is running from a docker container


Prefect Cloud/Additional Resources
* docs.prefect.io
* app.prefect.cloud
    * Additional workspaces, each workspace has core prefect features, automation features, get 3 free users, etc.
* GitHub.com/anna-geller
* Discourse.prefect.io