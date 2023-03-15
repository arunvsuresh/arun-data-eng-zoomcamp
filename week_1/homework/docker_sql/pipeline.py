#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import sys
from sqlalchemy import create_engine
import pandas as pd
from time import time
import json
# get_ipython().system('pip install psycopg2')

f = open('env_vars.json')
data = json.load(f)

def main(params):
    user = data['user']
    password = data['password']

    print('password', password)
    host = params.host
    port = params.port
    db = params.db
    # table_name = params.table_name
    # url = params.url
    green_taxi_url = data['green_taxi_url']
    zone_url = data['zone_url']

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    engine.connect()

    # INGEST ZONE DATA 
    # if 'zone' in url:
    # table_name = 'zones'
    zones_csv_name = 'zones.csv'

    os.system(f"wget {zone_url} -O {zones_csv_name}")


    df = pd.read_csv(zones_csv_name)

    # df = next(zone_df_iter)

    # df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)

    # df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    start = time()
    df.to_sql(name='zones', con=engine, if_exists='replace')
    end = time()

    print('inserted zones...took %.3f second(s)' % (end - start))

    # INGEST GREEN TAXI TRIPS DATA
    # else:
    # table_name = 'green_taxi_trips'
    compressed_csv_name = 'green_taxi.csv.gz'
    # uncompressed_csv_name = 'green_taxi.csv'


    os.system(f"wget {green_taxi_url} -O {compressed_csv_name}")
    os.system(f"gunzip {compressed_csv_name}")
    csv_name = [file for file in os.listdir(os.getcwd()) if 'green_taxi' in file][0]
    print('csv name', csv_name)

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, low_memory=False)

    df = next(df_iter)

    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)

    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    df.head(n=0).to_sql(name='green_taxi_trips', con=engine, if_exists='replace')
    print(f"created table: green_taxi_trips")

    start = time()

    df.to_sql(name='green_taxi_trips', con=engine, if_exists='append')

    end = time()
    print('inserted another chunk... took %.3f second(s)' % (end - start))

    while True:
        start = time()

        try:
            df = next(df_iter)

            # df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)

            # df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

            df.to_sql(name='green_taxi_trips', con=engine, if_exists='append')

            end = time()
            print('inserted another chunk..., took %.3f second(s)' % (end - start))
        except StopIteration:
            print('finished data ingestion to postgres')
            break


if __name__== '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # user, password, host, port, database name, table name, url of csv
    # parser.add_argument('--user', help='user name for postgres')
    # parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    # parser.add_argument('table_name', help='name of table to results to')
    # parser.add_argument('--url', help='url of csv file')

    args = parser.parse_args()

    main(args)