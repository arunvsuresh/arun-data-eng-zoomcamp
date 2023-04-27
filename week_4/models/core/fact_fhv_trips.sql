{{ config(materialized='table') }}

with trip as (
    select *, 
        'Fhv' as service_type 
    from {{ ref('stg_fhv_tripdata') }}
),

dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)
select 

    trip.dispatching_base_num,
    trip.pickup_datetime,
    trip.dropOff_datetime,
    trip.SR_Flag,
    trip.Affiliated_base_number,
    trip.pickup_locationid,
    trip.dropoff_locationid,

     
    pickup_zone.borough as pickup_borough, 
    pickup_zone.zone as pickup_zone, 
    
    dropoff_zone.borough as dropoff_borough, 
    dropoff_zone.zone as dropoff_zone,  
    
    
from trip
inner join dim_zones as pickup_zone
on trip.pickup_locationid = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on trip.dropoff_locationid = dropoff_zone.locationid