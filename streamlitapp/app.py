import streamlit as st
import pandas as pd

# Page Infos
st.set_page_config(
    page_title="smart weather CH",
    page_icon="🌤️"
)

# Titel
st.title(
    "Smart Weather CH",
    anchor=False,                # kein Anker-Icon
    width="stretch"              # "stretch" = volle Breite nutzen
)

# subtitle
st.subheader("Wilkommen zur Smart Weather CH Ihre persönliche Wetterquelle")

# columns
col1, col2 = st.columns([4, 1])

with col1:
    query = st.text_input(
        "Suche",                      # interner Label-Text (für Screenreader)
        placeholder="Suchbegriff...", # das ist der sichtbare Text
        label_visibility="collapsed"  # Label ausblenden
    )

with col2:
    querry_button = st.button("Suchen")
