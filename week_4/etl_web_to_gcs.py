import io
import os
import requests
import pandas as pd
import pyarrow
import yaml
from timeit import default_timer as timer



from google.cloud import storage

BUCKET = os.environ.get("GCP_GCS_BUCKET")

def upload_files_to_gcs(bucket_name, local_file_name, destination):
    """Uploads a local file to GCS bucket."""

    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination)

    try:
        blob.upload_from_filename(local_file_name)

        print(
            f"File {local_file_name} uploaded to {destination}.\n"
        )
    except Exception as e:
        print(f'failed to upload bucket: {e}\n')

def extract_and_transform_from_web(service_type):

    """
        Extract and transform:
        Yellow taxi data - Years 2019 and 2020
        Green taxi data - Years 2019 and 2020
        fhv data - Year 2019.
    """

    years = []
    months = [month for month in range(1, 13)]
    base_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"

    if service_type == 'green' or service_type == 'yellow':
        years.extend((2019, 2020))

        for year in years:
            print(f'parsing {service_type} data\n')
            parse_web_url(service_type, year, months, base_url)

    else:
        years = 2019
        print(f'parsing {service_type} data\n')
        parse_web_url(service_type, years, months, base_url)



def parse_web_url(service_type, year, months, base_url):
     for month in months:
        start = timer()
        dataset_file = f"{service_type}_tripdata_{year}-{month:02}.csv.gz"

        dataset_url = f"{base_url}/{service_type}/{dataset_file}"

        # get file from web and output it to .csv.gz file
        os.system(f"wget {dataset_url} -O {dataset_file}")

        # look for newly downloaded gzip file
        gz_files = [file for file in os.listdir() if file.endswith(".csv.gz")]

        # unzip .gz file
        os.system(f"gunzip {gz_files[0]}")

        # look for unzipped csv file
        files = [file for file in os.listdir() if file.endswith(".csv")]

        dataset_file = files[0]

        # read file schemas from external yaml file
        with open("vehicle_schemas.yml", mode="rb") as file:
            schemas = yaml.safe_load(file)

        # read file into csv via pandas and change schema
        df = pd.read_csv(dataset_file).astype(schemas[service_type])

        dataset_file = dataset_file.replace('.csv', '.parquet')

        # convert to parquet
        df.to_parquet(dataset_file, engine='pyarrow')

        print(f"converted to parquet: {dataset_file}\n")

        upload_files_to_gcs(BUCKET, dataset_file, f"data/{service_type}/{dataset_file}")

        end = timer()

        print(f'took {(end - start) / 60} minute(s) to parse and upload {month}/{year} {service_type} file\n')

        os.system(f"rm {files[0]}")
        print(f'removed csv file: {files[0]}\n')

        os.system(f"rm {dataset_file}")
        print(f'removed parquet file: {dataset_file}\n')


if __name__ == '__main__':
    service_types = ['fhv', 'green', 'yellow']
    for service_type in service_types:
        extract_and_transform_from_web(service_type)