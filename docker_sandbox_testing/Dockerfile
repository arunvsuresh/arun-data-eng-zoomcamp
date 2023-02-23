FROM python:3.9.1

# RUN apt-get install wget
RUN pip install pandas

# current directory to go into
# once docker image is run
WORKDIR /app
# copied pipeline file from local
# to remote machine
COPY pipeline.py pipeline.py

ENTRYPOINT [ "python", "pipeline.py"]