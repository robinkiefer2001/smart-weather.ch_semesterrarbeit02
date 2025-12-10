import streamlit as st
import pandas as pd

# Page Infos
st.set_page_config(
    page_title="smart weather CH",
    page_icon="🌤️",
    layout="wide"
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

# --- Dummy-Daten ---
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
window_size = 5           # mind. 5 Tage sichtbar
radius = window_size // 2

# --- Session State für die aktuelle Position ---
if "center" not in st.session_state:
    st.session_state.center = 0  # Start beim ersten Tag

# --- Navigation: Pfeile links/rechts ---
nav_left, nav_mid, nav_right = st.columns([1, 3, 1])
with nav_left:
    if st.button("<"):
        st.session_state.center = (st.session_state.center - 1) % n
with nav_right:
    if st.button(">"):
        st.session_state.center = (st.session_state.center + 1) % n

center = st.session_state.center

# --- Indizes der 5 sichtbaren Tage (zirkulär) ---
indices = [(center + i) % n for i in range(-radius, radius + 1)]

# Mittlere Spalte breiter machen, damit sie „im Vordergrund“ wirkt
# Beispiel: 1 – 2 – 3 – 2 – 1
col_widths = [1, 2, 3, 2, 1]

cols = st.columns(col_widths, border=True, gap="small")

for col, idx in zip(cols, indices):
    with col:
        if idx == center:
            # Center-Block: größer & fett
            st.markdown(
                f"### {tage[idx]}",
                help="Aktueller Tag im Fokus"
            )
        else:
            st.write(tage[idx])

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

import streamlit.components.v1 as components

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

  // Swisstopo / Swiss Base Map (vereinfachtes Beispiel)
  // ACHTUNG: Für produktiven Einsatz unbedingt Terms of Use beachten!
  // [Hier als Demo: OpenStreetMap als Basiskarte]
  L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors'
    }
  ).addTo(map);

  // -------------------------------------------
  // Platzhalter für MeteoSwiss / WMTS-Radar-Layer
  // -------------------------------------------
  // Wenn du eine WMTS-Tile-URL aus wmts.geo.admin.ch
  // oder MeteoSwiss-Open-Data hast, kommt sie hier rein,
  // z.B. (syntaktisch! URL musst du aus den Capabilities nehmen):

  /*
  L.tileLayer(
    'https://wmts{5-9}.geo.admin.ch/1.0.0/<LAYERNAME>/default/<TIMESTAMP>/21781/{z}/{x}/{y}.png',
    {
      opacity: 0.7,
      attribution: 'MeteoSwiss / geo.admin.ch'
    }
  ).addTo(map);
  */

  // Stattdessen ein Fake-Radar-Layer (halbtransparentes Grid) zum Testen:
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