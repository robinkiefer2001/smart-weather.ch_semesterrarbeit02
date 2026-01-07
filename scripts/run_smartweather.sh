#!/bin/bash
REPO_DIR="/opt/smartweather_repo"
DEPLOY_DIR="/opt/streamlit"

cd "$REPO_DIR"
git fetch origin main
git checkout origin/main -- streamlitapp/

# Kopiere alle Python-Module
cp "$REPO_DIR/streamlitapp/"*.py "$DEPLOY_DIR/"

cd "$DEPLOY_DIR"
source venv/bin/activate
exec streamlit run app.py --server.port=8501 --server.address=0.0.0.0