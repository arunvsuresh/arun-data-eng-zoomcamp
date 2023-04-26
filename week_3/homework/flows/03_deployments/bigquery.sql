-- CREATE OR REPLACE EXTERNAL TABLE `dtc-de-380020.nytaxi.taxi-rides`
-- OPTIONS (
--   format = 'CSV',
--   uris = ['gs://zoomcamp_prefect_bucket/data/fhv_tripdata_2019-*.csv.gz']
-- );


-- CREATE OR REPLACE EXTERNAL TABLE `dtc-de-380020.nytaxi.fhv`
-- OPTIONS (
--   format = 'PARQUET',
--   uris = ['gs://zoomcamp_prefect_bucket/data/fhv/*']
-- );

-- CREATE OR REPLACE TABLE `dtc-de-380020.nytaxi.taxi-rides_non_partitioned` AS
-- SELECT * FROM `dtc-de-380020.nytaxi.taxi-rides`;

CREATE OR REPLACE EXTERNAL TABLE `dtc-de-380020.nytaxi.external_fhv`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://zoomcamp_prefect_bucket/data/fhv/*']
);

CREATE OR REPLACE TABLE `dtc-de-380020.nytaxi.fhv` AS
SELECT * FROM `dtc-de-380020.nytaxi.external_fhv`;



CREATE OR REPLACE EXTERNAL TABLE `dtc-de-380020.nytaxi.external_green`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://zoomcamp_prefect_bucket/data/green/*']
);

CREATE OR REPLACE TABLE `dtc-de-380020.nytaxi.green` AS
SELECT * FROM `dtc-de-380020.nytaxi.external_green`;



CREATE OR REPLACE EXTERNAL TABLE `dtc-de-380020.nytaxi.external_yellow`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://zoomcamp_prefect_bucket/data/yellow/*']
);

CREATE OR REPLACE TABLE `dtc-de-380020.nytaxi.yellow` AS
SELECT * FROM `dtc-de-380020.nytaxi.external_yellow`;

drop table `dtc-de-380020.nytaxi.external_fhv`;
drop table `dtc-de-380020.nytaxi.external_green`;
drop table `dtc-de-380020.nytaxi.external_yellow`;

