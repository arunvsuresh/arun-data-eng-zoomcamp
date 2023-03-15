#!/usr/bin/env python
# coding: utf-8

import argparse
import sys
from sqlalchemy import create_engine
import pandas as pd
from time import time

# get_ipython().system('pip install psycopg2')

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name

    csv_name = 'output.csv'



    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    engine.connect()

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)

    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')


    while True:
        start = time()
        df = next(df_iter)

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)

        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists='append')

        end = time()
        print('inserted another chunk..., took %.3f second' % (end - start))


if __name__== '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # user, password, host, port, database name, table name, url of csv
    parser.add_argument('user', help='user name for postgres')
    parser.add_argument('password', help='password for postgres')
    parser.add_argument('host', help='host for postgres')
    parser.add_argument('port', help='port for postgres')
    parser.add_argument('db', help='database name for postgres')
    parser.add_argument('table_name', help='name of table to results to')
    parser.add_argument('url', help='url of csv file')

    args = parser.parse_args()

    main(args)