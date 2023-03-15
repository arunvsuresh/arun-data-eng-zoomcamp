## Week 1 - Docker, Postgres, GCP, Terraform

<!-- * [Introduction to Docker](#de-zoomcamp---introduction-to-docker) -->

#### Docker

What is docker?
*  “Delivers software in the form of containers”. “Containers are isolated from one another”. Containers are independent execution environments that contain everything application needs: OS, system libraries, packages, etc.

* Why should we care about docker?
    * Reproducibility
    * Running local experiments
    * Running local tests (integration) (CI/CD)
        * e.g. data pipeline and have expected result from pipeline…can run tests to confirm expected behavior of pipeline
    * Running pipelines on cloud (AWS batch, Kubernetes jobs)
    * Spark - can specify dependencies we need for our data pipeline in spark with docker
    * serverless (AWS lambda)

* Docker image
    * Snapshot of your container
    * Has all the instructions needed to setup particular env
    * Can take your docker image and run it in a different env (e.g. AWS or Google Cloud)
    * Enables 100% reproducibility b/c initial image and image used in cloud env are identical

* Dockerfile
    * file containing set of instructions for Docker to execute upon a building an image

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
    * whatever dockerfile contains as its entrypoint, we run that command/executable, e.g. a ‘bash’ entrypoint results in bash prompt after running ^above command


<!-- * [Introduction to Postgres](#de-zoomcamp---introduction-to-postgres) -->
