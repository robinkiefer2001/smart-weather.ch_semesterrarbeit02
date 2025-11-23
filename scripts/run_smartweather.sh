#!/bin/bash

# Repo und Deploy-Verzeichnis definieren
REPO_DIR="/opt/smartweather_repo"
DEPLOY_DIR="/opt/streamlit"

# Wechsle ins Repo und update den Code
cd "$REPO_DIR"
git fetch origin main
git checkout origin/main -- streamlitapp/app.py

# app.py ins Deploy-Ziel kopieren (ggf. Rechte beibehalten)
cp "$REPO_DIR/streamlitapp/app.py" "$DEPLOY_DIR/app.py"

# Streamlit starten
cd "$DEPLOY_DIR"
source venv/bin/activate
exec streamlit run app.py --server.port=8501 --server.address=0.0.0.0
