import argparse
from sqlalchemy import create_engine
import pyarrow.parquet as pq
import os
from time import time
from tqdm import tqdm

# url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"

# table_name = 'yellow_taxi_data'

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # connect to postgres engine via passed-in args
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()


    file_name = 'output.parquet'

    # download file
    os.system(f"wget {url} -O {file_name}")
    # read parquet file
    parquet_file = pq.ParquetFile(file_name)

    # get size of parquet file
    parquet_size = parquet_file.metadata.num_rows
    print('file size...', parquet_size, ' rows')

    pq.read_table(file_name).to_pandas().head(0).to_sql(name=table_name, con=engine, if_exists='replace')

    print(f"table {table_name} created...")

    batch_size = 64_000
    current_batch = batch_size
    total_start = time()

    with tqdm(total=parquet_size, unit='steps', unit_scale=True) as pbar:
        for i in parquet_file.iter_batches(use_threads=True):
            # start = time()
            print(f'ingesting {current_batch} out of {parquet_size} rows')
            i.to_pandas().to_sql(name=table_name, con=engine, if_exists='append')
            current_batch += batch_size
            pbar.update(batch_size)
        pbar.update(current_batch)
    total_end = time()
    print(f"took total of %.1f seconds" % (total_end - total_start))


if __name__== '__main__':
    parser = argparse.ArgumentParser(description='Ingest file data to Postgres')

    # user, password, host, port, database name, table name, url of csv
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of table to results to')
    parser.add_argument('--url', help='url of file')

    args = parser.parse_args()

    main(args)









# pq.read_table(output_name).to_pandas().head(0).to_sql(name=table_name, con=engine, if_exists='replace')

# batch_size = 65536

# for i in parquet_file.iter_batches(use_threads=True):
#     print("RecordBatch")
#     print(i.to_pandas())

#     start = time()
#     # df = next(df_iter)

#     # df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)

#     # df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

#     print(f'ingesting {batch_size} out of {parquet_size} rows ({index / parquet_size:.0%})')

#     i.to_pandas().to_sql(name=table_name, con=engine, if_exists='append')

#     batch_size += batch_size

#     df.to_sql(name=table_name, con=engine, if_exists='append')

#     end = time()