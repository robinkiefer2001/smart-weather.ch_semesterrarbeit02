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

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1:
    st.write("Mo")
    st.metric("Temperatur", "22 °C", "+1 °C", wind_speed_10m="up")

with col2:
    st.write("Di")
    st.metric("Temperatur", "21 °C", "-1 °C", wind_speed_10m="down")

with col3:
    st.write("Mi")
    st.metric("Temperatur", "19 °C", "-2 °C", wind_speed_10m="down")

with col4:
    st.write("Do")
    st.metric("Temperatur", "20 °C", "+1 °C", wind_speed_10m="up")

with col5:
    st.write("Fr")
    st.metric("Temperatur", "18 °C", "-2 °C", wind_speed_10m="down")

with col6:
    st.write("Sa")
    st.metric("Temperatur", "17 °C", "-1 °C", wind_speed_10m="down")

with col7:
    st.write("So")
    st.metric("Temperatur", "16 °C", "-1 °C", wind_speed_10m="down")
    
