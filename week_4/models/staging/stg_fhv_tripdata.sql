{{ config(materialized='view') }}

with tripdata as 
(
  select *
  from {{ source('staging', 'fhv') }}
)

select

    dispatching_base_num,
    pickup_datetime,
    dropOff_datetime,
    SR_Flag,
    Affiliated_base_number,


    cast(PUlocationID as integer) as pickup_locationid,
    cast(DOlocationID as integer) as dropoff_locationid,
    

from tripdata

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=false) %}

  limit 100

{% endif %}