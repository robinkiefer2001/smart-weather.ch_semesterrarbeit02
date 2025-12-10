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

st.markdown("### 7-Tage Wettervorhersage für Zürich")

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

with col1:
    st.write("Mo")
    st.metric(label="Temperatur", value="22 °C", delta="+1 °C")
    st.metric(label="Wind", value="10 km/h", delta="+2 km/h")

with col2:
    st.write("Di")
    st.metric(label="Temperatur", value="21 °C", delta="-1 °C")
    st.metric(label="Wind", value="8 km/h", delta="-1 km/h")

with col3:
    st.write("Mi")
    st.metric(label="Temperatur", value="19 °C", delta="-2 °C")
    st.metric(label="Wind", value="12 km/h", delta="+3 km/h")

with col4:
    st.write("Do")
    st.metric(label="Temperatur", value="20 °C", delta="+1 °C")
    st.metric(label="Wind", value="11 km/h", delta="-1 km/h")

with col5:
    st.write("Fr")
    st.metric(label="Temperatur", value="18 °C", delta="-2 °C")
    st.metric(label="Wind", value="9 km/h", delta="-2 km/h")

with col6:
    st.write("Sa")
    st.metric(label="Temperatur", value="17 °C", delta="-1 °C")
    st.metric(label="Wind", value="7 km/h", delta="-1 km/h")

with col7:
    st.write("So")
    st.metric(label="Temperatur", value="16 °C", delta="-1 °C")
    st.metric(label="Wind", value="6 km/h", delta="-1 km/h")

