# assets.py
import os
import duckdb
import requests
import pandas as pd
import subprocess
from dagster import asset

API_KEY = "21bf85af6585b3f13d8adf7a26cbd415591556ac7f77030212f6584dabd63efe"
BASE_URL = "https://api.meteo-concept.com/api/forecast/daily"

@asset
def raw_weather_data():
    print("ETAPE 1 : Extraction depuis l'API météo")
    params = {"token": API_KEY, "insee": "75056"}
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

@asset
def stored_weather_data(raw_weather_data):
    print("ETAPE 2 : Stockage dans DuckDB")
    db_path = os.path.join(os.getcwd(), "weather.duckdb")
    con = duckdb.connect(db_path)
    df = pd.DataFrame(raw_weather_data["forecast"])
    con.execute("CREATE TABLE IF NOT EXISTS weather AS SELECT * FROM df LIMIT 0")
    con.execute("DELETE FROM weather")
    con.execute("INSERT INTO weather SELECT * FROM df")
    con.close()
    return "✅ Données stockées dans DuckDB"

@asset(deps=["stored_weather_data"])
def run_dbt_asset():
    print("ETAPE 3 : Exécution de dbt run + test")
    dbt_path = os.path.join(os.getcwd(), "venv", "Scripts", "dbt.exe")
    dbt_project_path = os.path.join(os.getcwd(), "weather_dbt")
    subprocess.run([dbt_path, "run"], check=True, cwd=dbt_project_path)
    subprocess.run([dbt_path, "test"], check=True, cwd=dbt_project_path)
