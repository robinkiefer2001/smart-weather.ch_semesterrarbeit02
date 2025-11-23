import streamlit as st
import pandas as pd

# Titel
st.title("Smart Weather CH")

# Leere Tabelle anlegen
df = pd.DataFrame(columns=["Temperatur", "Windgeschwindigkeit", "Stadt"])

# Leere Tabelle anzeigen
st.dataframe(df)
