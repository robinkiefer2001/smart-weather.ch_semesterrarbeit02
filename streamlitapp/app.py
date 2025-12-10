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

st.set_page_config(layout="wide")

tage = ["Mo1", "Di1", "Mi1", "Do1", "Fr1", "Sa1", "So1",
        "Mo2", "Di2", "Mi2", "Do2", "Fr2", "Sa2", "So2"]

temperaturen = [22, 21, 19, 20, 18, 17, 16,
                23, 22, 20, 19, 18, 17, 16]
temp_delta   = [+1, -1, -2, +1, -2, -1, -1,
                +1, -1, -2, -1, -1, -1,  0]

windspeed    = [10, 8, 12, 11, 9, 7, 6,
                11, 9, 13, 12, 10, 8, 7]
wind_delta   = [+2, -1, +3, -1, -2, -1, -1,
                +1, -1, +2, -1, -1, -1,  0]

n = len(tage)

# Mittelpunkt des Karussells (0–13)
center = st.slider("Tag wählen", 0, n - 1, 0)

# Wie viele Tage insgesamt anzeigen (muss ungerade sein: 5, 7, ...)
window_size = 5
radius = window_size // 2  # z.B. 2 links, 2 rechts

# Indizes im Karussell (zirkulär)
indices = [ (center + i) % n for i in range(-radius, radius + 1) ]

cols = st.columns(window_size)

for col, idx in zip(cols, indices):
    with col:
        # Hervorheben des „vorderen“ Tages
        if idx == center:
            st.markdown(f"### {tage[idx]}")   # vorne, größer
        else:
            st.write(tage[idx])               # hinten, kleiner

        st.metric(
            label="Temperatur",
            value=f"{temperaturen[idx]} °C",
            delta=f"{temp_delta[idx]:+} °C",
        )

        st.metric(
            label="Wind",
            value=f"{windspeed[idx]} km/h",
            delta=f"{wind_delta[idx]:+} km/h",
        )
