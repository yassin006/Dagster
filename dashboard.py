import streamlit as st
import subprocess
import duckdb
import pandas as pd
import os
import pydeck as pdk

# --- Configuration de la page ---
st.set_page_config(page_title="Dashboard Météo Paris", layout="wide")
st.title("🌤️ Dashboard Météo - Paris")
st.subheader("📆 Prévisions journalières")

# --- Bouton d'actualisation des données ---
if st.button("📥 Actualiser les données"):
    with st.spinner("Mise à jour des données en cours..."):
        python_path = os.path.join("venv", "Scripts", "python.exe")
        result = subprocess.run([python_path, "main_pipeline.py"], capture_output=True, text=True)
        if result.returncode == 0:
            st.success("✅ Données mises à jour avec succès !")
            st.rerun()  # <- CORRIGÉ ICI
        else:
            st.error("❌ Échec de l'exécution du pipeline.")
            st.code(result.stderr)

# --- Chargement des données DuckDB ---
db_path = os.path.join(os.getcwd(), "weather.duckdb")
con = duckdb.connect(database=db_path, read_only=True)
df = con.execute("SELECT * FROM weather").fetchdf()
con.close()

# --- Formatage datetime ---
df["datetime"] = pd.to_datetime(df["datetime"])

# --- Mappage météo en emojis ---
weather_map = {
    0: "☀️ Clair", 1: "🌤️ Peu nuageux", 2: "⛅ Nuageux",
    3: "🌥️ Très nuageux", 4: "☁️ Couvert",
    5: "🌧️ Pluie", 6: "🌦️ Averse", 7: "⛈️ Orage",
    8: "🌨️ Neige", 9: "❄️ Verglas", 10: "🌫️ Brouillard"
}
df["conditions"] = df["weather"].map(weather_map)

# --- Sélecteur de jour ---
selected_day = st.selectbox("🗓️ Sélectionnez un jour", df["datetime"].dt.date.unique())
filtered_df = df[df["datetime"].dt.date == selected_day]

# --- Tableau météo ---
st.markdown("### 🧾 Données détaillées")
st.dataframe(
    filtered_df.style.format(subset=["tmin", "tmax", "rr10"], precision=1),
    height=300
)

# --- Carte interactive avec pydeck ---
st.markdown("### 🗺️ Carte météo interactive")
layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_df.dropna(subset=["latitude", "longitude"]),
    get_position='[longitude, latitude]',
    get_fill_color='[0, 128, 255, 160]',
    get_radius=100,
    pickable=True,
)
tooltip = {
    "html": "Jour: {day}<br>Tmax: {tmax}°C<br>Tmin: {tmin}°C<br>{conditions}",
    "style": {"backgroundColor": "black", "color": "white"}
}
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v10",
    initial_view_state=pdk.ViewState(
        latitude=filtered_df["latitude"].mean(),
        longitude=filtered_df["longitude"].mean(),
        zoom=10,
        pitch=0,
    ),
    layers=[layer],
    tooltip=tooltip
))

# --- Graphique température ---
st.markdown("### 🌡️ Température Max/Min")
st.line_chart(df[["datetime", "tmin", "tmax"]].set_index("datetime"))

# --- Graphique précipitations ---
st.markdown("### 🌧️ Précipitations (mm)")
st.bar_chart(df[["datetime", "rr10"]].set_index("datetime"))

# --- Résumé conditions météo ---
st.markdown("### 📋 Résumé des conditions météo")
for _, row in filtered_df.iterrows():
    st.write(
        f"{row['datetime'].date()} : {row['conditions']} – Tmin : {row['tmin']}°C | "
        f"Tmax : {row['tmax']}°C | Pluie : {row['rr10']} mm"
    )
