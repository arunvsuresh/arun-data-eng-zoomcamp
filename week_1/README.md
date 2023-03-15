DOCKER 
What is docker?
*  “Delivers software in the form of containers”. “Containers are isolated from one another”. Containers are independent execution environments that contain everything application needs: OS, system libraries, packages, etc.
* Docker image
    * Snapshot of your container 
    * Has all the instructions needed to setup particular env
    * Can take your docker image and run it in a different env (e.g. AWS or Google Cloud) 
    * Enables 100% reproducibility b/c initial image and image used in cloud env are identical
* Why should we care about docker?
    * Reproducibility
    * Running local experiments
    * Running local tests (integration) (CI/CD)
        * e.g. data pipeline and have expected result from pipeline…can run tests to confirm expected behavior of pipeline
    * Running pipelines on cloud (AWS batch, Kubernetes jobs)
    * Spark - can specificy dependencies we need for our data pipeline in spark with docker
    * serverless (AWS lambda)
Docker commands
* docker run -it ubuntu bash 
    * “run” runs docker image 
    * “-it" means interactive
    * Ubuntu is the linux distro (name of image you want to run)
    * Bash - shell command we want to execute in this image, provides bash prompt to execute commands
* docker run -it --entrypoint=bash python:3.9
    * Entrypoint- what gets executed when we run this container
*  docker build -t test:pandas .
    * Builds image from docker file
    * “-t" indicates tag —> test:pandas is name of image (tag)
    * “.” Means to build image in current directory
*  docker run -it test:pandas
    * B/c dockerfile contains ‘bash’ entrypoint, we get bash prompt after running ^above command


POSTGRES

*  Running Postgres with docker
    * docker run -it -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB="ny_taxi" -v ny_taxi_postgres_data:/var/lib/postgresql/data -p 5432:5432 postgres:13

    * NOTE
      * CLEAR ALL DOCKER CONTAINERS/VOLUMES/IMAGES, delete host folder, re-create host folder, change host folder permissions to read/write sudo chmod a+rwx <folder name>
      * Only specify folder name in volume param of docker run:  -v <folder_name>:/var/lib/postgresql/data
*  “-e” refers to env vars - way of configuring whatever we have in docker container
    *     What user will be, what password for user will be
* -v refer to volumes  - map folder  in our host filesystem to folder in container — since Postgres is a db, it needs to keep files in filesystem, this is also known as mounting
* -p refers to port - need to map a port from our host machine to port on container...  needed to send requests to our Postgres db, we will send sql queries to this db…need to be able to access specific port of Postgres  

*  Running Postgres through command line (pgcli):
    * pgcli -h localhost -p 5432 -u root -d ny_taxi
* Output first ’n’ rows of a dataset and save it to a diff file
    * head -n 100 yellow_tripdata_2021-01.csv > yellow_head.csv
* Wc -l <filename>
    * Counts no. of lines/rows in dataset

*NOTE
*  Localhost for docker container is container name itself…there is no Postgres running there on said container…need to run INSIDE docker network


Dockerizing ingestion script/docker compose
  * More to come soon!

Terraform
*  What is terraform?
    * Automate/manage infra & platform/services that run on that infra
    * Open source
    * Declarative - define end result you want
    * Tool for infra provisioning
        * Provisioning infra
            * Where terraform comes in 
            * e.g. create vpc, create aws users/permissions, spin up servers, install docker, etc...
        * Deploying apps
* Managing existing infra
    * Can easily Create infra
    * Can easily make Changes to infra
* Replicating infra
    * Can use terraform and identical infra/setup using same terraform code used for dev setup to produce prod setup
* Specifics of terraform files
    * locals
        * constants
    * variables
        * Generally Passed at run-time
        * With default - optional run-time args
        * Without default - mandatory run-time args

Port Mapping & Networks in Docker
*  Within host machine have docker container(s)
    * Run inside a docker compose file, so run inside same network
    * e.g. pgadmin talks to postgres
* In docker compose also have port mapping
    * Postgres it is 5432, pgadmin is 80
    * Have bunch of ports on host machine
    * We can map port on host machine to port on container—> -p 5432:5432
* If for example Postgres is running on host machine with a specific port, can do mapping/port forwarding to/from a different port
    * e.g. -p 5431:5432
* ingestion
    * Ingestion script goes directly to docker container so we don’t need to think about port mapping, use default Postgres port, which is 5432
    * e.g. docker run -it —port:5432 instead of another port
