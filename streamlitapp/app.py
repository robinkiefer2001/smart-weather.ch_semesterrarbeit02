import streamlit as st
import psycopg2
import psycopg
import datetime
import streamlit_calendar
import streamlit.components.v1 as components
import pandas as pd
from streamlit_calendar import calendar  # neues Package
conn = st.connection("sql")

# Variabel vereinbahurng
heute = datetime.date.today()


# Page Infos
st.set_page_config(
    page_title="smart weather CH",
    page_icon="🌤️",
    layout="wide"
)

st.title(
    "Smart Weather CH",
    anchor=False  # kein Anker-Icon
)


# subtitle
st.subheader("Wilkommen zur Smart Weather CH – Ihre persönliche Wetterquelle")

# Suche
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    query = st.text_input(
        "Suche",                       # interner Label-Text (für Screenreader)
        placeholder="Suchbegriff...",  # sichtbarer Text
        label_visibility="collapsed"   # Label ausblenden
    )

with col2:
    query_button = st.button("Suchen")

with col3:
    st.write("")

tempData = conn.query(
    "SELECT * FROM weather_current WHERE id = 1;",
    ttl="10m"   # Cache-Dauer, optional
)

# Minimale Optionen: Monatsansicht + klickbare Tage
calendar_options = {
    "initialView": "dayGridMonth",  # Monatsansicht
    "selectable": True,             # Klick auf Datum / Bereich
}

# 3 Spalten
col1, col2 = st.columns(2,1, border=True, gap="small")

with col1:
    st.metric(
        label="Lufttemperatur",
        value=f"{tempData['temperature_2m'][0]} °C",
    )

with col2:
    box1 = st.container()
    with box1:
        cal_data = calendar(
        options={"initialView": "dayGridMonth", "selectable": True},
        key="smartweather_calendar",
        )
    
    box2 = st.container()
    with box2: 
        st.metric(
            label="Niederschlag",
            value=f"{tempData['precipitation_sum'][0]} mm",
        )

col1, col2 = st.columns(1,2, border=True)
with col1:
    st.write(
        "Am Morgen in den Niederungen gebietsweise Nebel oder "
        "Tieflagenbewölkung, lokal auch Hochnebel. Im Laufe des "
        "Vormittags allmähliche Auflösung. Tagsüber meist sonnig mit "
        "einzelnen hohen Wolkenfeldern. In den Alpen stellenweise "
        "Föhnwolken. Am Nachmittag im Westen und Süden vermehrt "
        "hochreichende Wolkenfelder. Temperatur am Nachmittag um 20 "
        "Grad im Flachland, in den Bergen auf 2000 Metern um 8 Grad. "
        "In den Alpen mässiger bis starker Föhnwind, sonst meist "
        "leichter bis mässiger Wind aus Südwest bis West."
    )
with col2:
    leaflet_html = """
    <div id="map" style="width: 100%; height: 650px;"></div>

    <!-- Leaflet CSS & JS -->
    <link
      rel="stylesheet"
      href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

    <script>
      // Karte initialisieren (Schweiz-Zentrum)
      var map = L.map('map').setView([46.8, 8.3], 7);

      // Basiskarte (hier OSM als Demo)
      L.tileLayer(
        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        {
          maxZoom: 19
        }
      ).addTo(map);

      // Fake-Radar-Overlay als Platzhalter
      var bounds = L.latLngBounds(L.latLng(45.5, 5.5), L.latLng(48.0, 11.0));
      var overlay = L.rectangle(bounds, {
        color: "#00aaff",
        weight: 1,
        fillOpacity: 0.15
      }).addTo(map);
      overlay.bindPopup("Radar / Meteo-Layer Platzhalter");
    </script>
    """

    components.html(leaflet_html, height=700)