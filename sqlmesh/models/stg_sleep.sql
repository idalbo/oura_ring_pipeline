MODEL (
  name stg_oura.stg_sleep,
  kind FULL,
  cron '@daily',
  grain item_id,
);

SELECT
  day,
  sum(deep_sleep_duration) AS deep_sleep,
FROM
  oura.oura_ring_data.sleep
GROUP BY 
    day
  