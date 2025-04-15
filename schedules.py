# schedules.py
from dagster import ScheduleDefinition, define_asset_job
from assets import raw_weather_data, stored_weather_data

daily_weather_job = define_asset_job(name="daily_weather_job")

daily_weather_schedule = ScheduleDefinition(
    job=daily_weather_job,
    cron_schedule="0 7 * * *"  # tous les jours à 7h du matin
)
