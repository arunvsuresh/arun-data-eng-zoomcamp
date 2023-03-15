FROM python:3.9



# install wget
RUN apt-get install wget

# install pandas
RUN pip install pandas sqlalchemy psycopg2 tqdm pyarrow

# location in container where we're copying the file to
WORKDIR /app

# copy file from host machine to remote docker container
COPY pipeline.py pipeline.py
COPY env_vars.json env_vars.json

#override default entrypoint with running of "python pipeline.py"
ENTRYPOINT ["python", "pipeline.py"]

