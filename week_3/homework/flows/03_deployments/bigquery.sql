CREATE OR REPLACE EXTERNAL TABLE `dtc-de-380020.nytaxi.taxi-rides`
OPTIONS (
  format = 'CSV',
  uris = ['gs://zoomcamp_prefect_bucket/data/fhv_tripdata_2019-*.csv.gz']
);

CREATE OR REPLACE TABLE `dtc-de-380020.nytaxi.taxi-rides_non_partitioned` AS
SELECT * FROM `dtc-de-380020.nytaxi.taxi-rides`;