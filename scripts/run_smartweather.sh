# Helperskript für Streamlit Servic Start

#!bin/bash

cd /opt/streamlit
source venv/bin/activate
exec streamlit run app.py --server.port=8501 --server.address=0.0.0.0