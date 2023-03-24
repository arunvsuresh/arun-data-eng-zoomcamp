from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint

@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas df"""
    # if randint(0, 1) > 0:
    #     raise Exception
    df = pd.read_csv(dataset_url)

    return df



@task(log_prints=True)
def clean(df = pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""

    if 'lpep_pickup_datetime' in df.columns or 'lpep_dropoff_datetime' in df.columns:


        df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
        df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
        print(df.head(2))
        print(f"columns: {df.dtypes}")
        print(f"rows: {len(df)}")

    elif 'tpep_pickup_datetime' in df.columns or  'tpep_dropoff_datetime' in df.columns:

        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
        print(df.head(2))
        print(f"columns: {df.dtypes}")
        print(f"rows: {len(df)}")

    return df


@task()
def write_local(df:pd.DataFrame, color:str, dataset_file:str) -> Path:
    """Write dataframe out as a parquet file"""
    print('COLOR: ', color)
    print('DATASET FILE: ', dataset_file)
    # create a filepath to parquet file
    path = Path(f"data/{color}/{dataset_file}.parquet")
    # check to see if data/yellow exists as a parent to parquet file
    # if not, create them
    print('path parent is dir: ', path.parent.is_dir())
    if not path.parent.is_dir():
        path.parent.mkdir(parents=True)
    print('PATH: ', path)
    df.to_parquet(path, compression='gzip')
    return path

@task()
def write_gcs(path: Path) -> None:
    """Uploading local parquet file to gcs"""
    gcp_block = GcsBucket.load("zoomcamp-gcs")
    gcp_block.upload_from_path(from_path=f"{path}", to_path=path)
    return

@flow()
def etl_web_to_gcs(month: int,
                   year: int,
                   color: str):
    """The main ETL function"""
    # color = "yellow"
    # year = 2021
    # month = 1
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"
    print('DATASET URL: ', dataset_url)
    # grab data and set to df
    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path)


# going to trigger this flow maybe x times for x months
# see for loop in function
@flow()
def etl_parent_flow(months: list[int] = [1, 2],
                    year: int = 2021,
                    color: str = 'yellow'):
    for month in months:
        etl_web_to_gcs(month, year, color)


if __name__ == '__main__':
    months = [1, 2, 3]
    year = 2021
    color = 'yellow'
    etl_parent_flow(months, year, color)