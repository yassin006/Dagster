import sys
import os
import pytest
import duckdb
import pandas as pd

# Ajout du chemin parent au path Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from assets import raw_weather_data, stored_weather_data

def test_raw_weather_data_format():
    """Vérifie que les données brutes contiennent les clés attendues."""
    data = raw_weather_data()
    assert "forecast" in data
    assert isinstance(data["forecast"], list)
    assert len(data["forecast"]) > 0

def test_stored_weather_data_in_duckdb():
    """Vérifie que les données ont bien été stockées dans DuckDB."""
    # Simule le stockage
    raw_data = raw_weather_data()
    stored_weather_data(raw_data)

    # Connexion à la base
    db_path = os.path.join(os.getcwd(), "weather.duckdb")
    con = duckdb.connect(database=db_path, read_only=True)
    df = con.execute("SELECT * FROM weather").fetchdf()
    con.close()

    # Vérifications simples
    assert not df.empty
    assert "tmin" in df.columns
    assert "tmax" in df.columns
    assert "datetime" in df.columns or "day" in df.columns  # selon ton modèle dbt
