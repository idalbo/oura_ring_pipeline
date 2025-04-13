MODEL (
  name stg_oura.stg_sleep,
  kind VIEW
);

WITH renamed as(

	  SELECT 
        date(day)                     AS date_day,
        id, 
        average_breath,
        average_heart_rate,
        average_hrv,
        awake_time,
        bedtime_end,
        bedtime_start,
        deep_sleep_duration,
        efficiency,
        heart_rate__interval,
        heart_rate__timestamp,
        hrv__interval,
        hrv__timestamp,
        latency,
        light_sleep_duration,
        lowest_heart_rate,
        movement_30_sec,
        period,
        readiness__contributors__body_temperature,
        readiness__contributors__previous_day_activity,
        readiness__contributors__previous_night,
        readiness__contributors__recovery_index,
        readiness__contributors__resting_heart_rate,
        readiness__score,
        readiness__temperature_deviation,
        readiness_score_delta,
        rem_sleep_duration,
        restless_periods,
        sleep_phase_5_min,
        sleep_score_delta,
        time_in_bed,
        total_sleep_duration,
        TYPE                          AS sleep_type,
        "_dlt_load_id",
        "_dlt_id",
        readiness__contributors__activity_balance,
        readiness__contributors__sleep_balance,
        readiness__temperature_trend_deviation,
        readiness__contributors__hrv_balance
    FROM 
        oura.oura_ring_data.sleep
    WHERE
        TYPE != 'sleep'
    QUALIFY
        row_number() over(PARTITION BY day ORDER BY COALESCE(time_in_bed, 0) DESC) = 1

)

SELECT 
    *
FROM 
    renamed
  