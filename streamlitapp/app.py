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

# 2 Spalten: links breit (Wetter-Metrics), rechts schmal (Kalender + Metric)
col1, col2 = st.columns([2, 1], border=True, gap="small")

# ---- linke Spalte: mehrere Metrics in Unter-Spalten ----
with col1:
    # ein Container für die aktuelle Station / den aktuellen Zeitpunkt
    box = st.container(border=False)

    with box:
        row = tempData.iloc[0]

        m1, m2, m3 = st.columns(3, gap="small")  # „sub columns“ im Container

        with m1:
            st.metric("🌡️ Lufttemperatur", f"{row['temperature_2m']:.1f} °C")
            st.metric("🥵 Gefühlte Temp.", f"{row['apparent_temperature']:.1f} °C")

        with m2:
            st.metric("💧 rel. Feuchte", f"{row['relative_humidity_2m']:.0f} %")
            st.metric("☁️ Bewölkung", f"{row['cloud_cover']:.0f} %")

        with m3:
            st.metric("🌬️ Wind 10 m", f"{row['wind_speed_10m']:.1f} km/h")
            st.metric("💨 Böen 10 m", f"{row['wind_gusts_10m']:.1f} km/h")

# ---- rechte Spalte: Kalender + extra-Metric ----
with col2:
    box1 = st.container(border=True)
    with box1:
        cal_data = calendar(
            options={"initialView": "dayGridMonth", "selectable": True},
            key="smartweather_calendar",
        )

    box2 = st.container(border=True)
    with box2:
        st.metric("🌧️ Niederschlag", f"{row['precipitation']:.1f} mm")


col1, col2 = st.columns([1, 2], border=True, gap="small")
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
      // Bounds für Schweiz‑Ausschnitt
      var bounds = L.latLngBounds(
        L.latLng(45.5, 5.5),   // Süd‑West
        L.latLng(48.0, 11.0)   // Nord‑Ost
      );

      // Karte auf diese Bounds zoomen und begrenzen
      var map = L.map('map', {
        maxBounds: bounds,
        maxBoundsViscosity: 1.0
      }).fitBounds(bounds);

      // Basiskarte (OSM)
      L.tileLayer(
        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        {
          maxZoom: 14,
          minZoom: 6
        }
      ).addTo(map);

      // Optional: nur Rahmen statt blauem Overlay
      L.rectangle(bounds, {
        color: "#00aaff",
        weight: 1,
        fillOpacity: 0.0     // 0 = kein Blau, nur Linie
      }).addTo(map);

      // Später kannst du hier deine Meteo‑Daten als Layer hinzufügen,
      // z.B. L.imageOverlay(imageUrl, bounds, {opacity: 0.6}).addTo(map);
    </script>
    """

    components.html(leaflet_html, height=700)