import streamlit as st
import pandas as pd

# Page Infos
st.set_page_config(
    page_titel="smart weather CH",
    page_icon="🌤️",
)

# Titel
st.title("Smart Weather CH")

# Leere Tabelle anlegen
df = pd.DataFrame(columns=["Temperatur", "Windgeschwindigkeit", "Stadt"])

# Leere Tabelle anzeigen
st.dataframe(df)
