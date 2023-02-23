FROM python:3.9

# install pandas
RUN pip install pandas

# location in container where we're copying the file to
WORKDIR /app

# copy file from host machine to remote docker container 
COPY pipeline.py pipeline.py

#override default entrypoint with running of "python pipeline.py"
ENTRYPOINT ["python", "pipeline.py"]

