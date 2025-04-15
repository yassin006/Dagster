import os
import requests
import duckdb
import pandas as pd
import subprocess
from dagster import job, op

API_KEY = "21bf85af6585b3f13d8adf7a26cbd415591556ac7f77030212f6584dabd63efe"
BASE_URL = "https://api.meteo-concept.com/api/forecast/daily"

@op
def fetch_weather_data():
    print("ETAPE 1 : Récupération météo depuis l'API")
    params = {
        "token": API_KEY,
        "insee": "75056"  # Paris
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    print("Données météo récupérées avec succès")
    return data

@op
def store_weather_data(data):
    print("ETAPE 2 : Stockage dans DuckDB")
    db_path = os.path.join(os.getcwd(), "weather.duckdb")
    con = duckdb.connect(database=db_path)

    forecasts = data.get("forecast", [])
    df = pd.DataFrame(forecasts)

    con.execute("CREATE TABLE IF NOT EXISTS weather AS SELECT * FROM df LIMIT 0")
    con.execute("DELETE FROM weather")
    con.execute("INSERT INTO weather SELECT * FROM df")
    con.close()
    print("Données stockées dans DuckDB")

@op
def run_dbt():
    print("ETAPE 3 : Lancement de dbt run + dbt test")
    dbt_path = os.path.join("venv", "Scripts", "dbt.exe")
    dbt_dir = os.path.join(os.getcwd(), "weather_dbt")

    subprocess.run([dbt_path, "run"], cwd=dbt_dir, check=True)
    subprocess.run([dbt_path, "test"], cwd=dbt_dir, check=True)


@job
def full_pipeline():
    data = fetch_weather_data()
    store_weather_data(data)
    run_dbt()

if __name__ == "__main__":
    def main():
        print("Lancement du pipeline complet...")
        result = full_pipeline.execute_in_process()
        if result.success:
            print("Pipeline exécuté avec succès")
        else:
            print("Erreur lors de l'exécution du pipeline")

    main()
