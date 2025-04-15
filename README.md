# 🌤️ Dagster Weather Pipeline

Un projet complet d'ingénierie des données pour extraire, transformer, stocker et visualiser des données météo.

## Fonctionnalités du pipeline

- 🔄 Extraction de données météo via l'API Météo Concept
- 🧊 Stockage dans une base de données locale DuckDB
- 🔧 Transformation des données avec `dbt`
- 📊 Visualisation interactive avec `Streamlit`
- ⚙️ Orchestration complète avec `Dagster`
- ✅ Tests unitaires avec `pytest`

---

## Technologies utilisées

| Technologie | Usage |
|-------------|-------|
| Python 3.11 | Langage principal |
| Dagster     | Orchestration du pipeline |
| dbt         | Transformation des données |
| DuckDB      | Stockage local |
| Streamlit   | Dashboard interactif |
| Pytest      | Tests Python |

---

## 🚀 Démarrage rapide

### 1. Cloner le projet

```bash
git clone https://github.com/yassin006/Dagster.git
cd Dagsterr
```

### 2. Créer l'environnement virtuel

```bash
python -m venv venv
.env\Scriptsctivate   # Sur Windows
source venv/bin/activate # Sur macOS/Linux
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Initialiser le projet dbt

```bash
cd weather_dbt
dbt deps
cd ..
```

---

## 🧪 Lancer les tests

```bash
pytest
```

## 🌐 Lancer le dashboard

```bash
streamlit run dashboard.py
```

## 🕓 Orchestration avec Dagster

```bash
dagster dev -f repository.py
```

Ouvre [http://localhost:3000](http://localhost:3000) pour voir Dagster.

---

## 🐳 Dockerisation 

Ajoute un `Dockerfile` et un `docker-compose.yml` pour tout conteneuriser.
