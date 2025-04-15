# repository.py
from dagster import Definitions, load_assets_from_modules
import assets  # on importe le module entier pour pouvoir charger les assets dynamiquement
from schedules import daily_weather_schedule

# Charger tous les assets du module assets
all_assets = load_assets_from_modules([assets])

# Définir le repository
defs = Definitions(
    assets=all_assets,
    schedules=[daily_weather_schedule],
)
