# FROM python:3.9



# # install wget
# RUN apt-get install wget

# # install pandas
# RUN pip install pandas sqlalchemy psycopg2 tqdm pyarrow

# # location in container where we're copying the file to
# WORKDIR /app

# # copy file from host machine to remote docker container
# COPY pipeline.py pipeline.py
# # COPY env_vars.json env_vars.json

# #override default entrypoint with running of "python pipeline.py"
# ENTRYPOINT ["python", "pipeline.py"]

FROM prefecthq/prefect:2.7.7-python3.9

# copy docker requirements file to current dir
COPY docker-requirements.txt .

# run pip install on docker requirements file and make sure pip doesn't install cached packages
RUN pip install -r docker-requirements.txt --trusted-host pypi.python.org --no-cache-dir

RUN mkdir -p /opt/prefect/data/
RUN mkdir -p /opt/prefect/data/yellow
RUN mkdir -p /opt/prefect/flows/


COPY flows/03_deployments /opt/prefect/flows