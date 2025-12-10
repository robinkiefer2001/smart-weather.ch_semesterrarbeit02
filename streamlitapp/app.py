import streamlit as st
import datetime
import streamlit.components.v1 as components
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


heute = datetime.date.today()

auswahl = st.date_input(
    "Datum auswählen",
    value=heute,              # Standard: heute
    min_value=heute,          # frühestes Datum
    max_value=heute.replace(year=heute.year + 1),  # spätestes Datum
    format="DD.MM.YYYY"       # Anzeigeformat
)

st.write("Gewähltes Datum:", auswahl)

col1, col2, col3 = st.columns(border=True, gap="small")

with col1:
    st.metric(
        label="Lufttemperatur",
        value="22 °C",
        delta="+2 °C",
    )

with col2:
    st.Text("Im Mittelland Nebel, Obergrenze um 600 Meter, bis am Nachmittag wahrscheinlich grösstenteils Auflösung. Darüber und in den Alpen und Voralpen meist sonnig. Von der Region Bern bis zur Nordwestschweiz mit zeitweise dichteren mittelhohen und hohen Wolkenfeldern nur teilweise sonnig. Am Abend aus Westen allgemein Bewölkungszunahme und in der Nacht besonders am Nordrand der Schweiz etwas Regen möglich. Temperatur am Nachmittag um 10 Grad. In den Bergen schwacher bis mässiger Südwestwind. Temperatur auf 2000 Metern bis am Abend auf rund 3 Grad sinkend.")

with col3:
    auswahl


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