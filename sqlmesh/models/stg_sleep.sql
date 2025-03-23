MODEL (
  name stg_oura.stg_sleep,
  kind INCREMENTAL_BY_TIME_RANGE (
    time_column day
  ),
  start '2021-02-01',
  cron '@daily',
  grain day,
);

SELECT
  day,
  sum(deep_sleep_duration) AS deep_sleep,
FROM
  oura_ring_data.sleep
GROUP BY 
  day
  