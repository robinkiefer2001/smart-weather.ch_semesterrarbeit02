import streamlit as st
import psycopg2
import psycopg
import datetime
import streamlit_calendar
import streamlit.components.v1 as components
import pandas as pd
from streamlit_calendar import calendar  # neues Package
#import requests_cache
#from retry_requests import retry
import requests
import openmeteo_requests

conn = st.connection("sql")
cur = None

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

if query:
    selectedLocation = conn.query(
        text("""
            SELECT latitude, longitude
            FROM geo_location
            WHERE name ILIKE :name
            LIMIT 1;
        """),
        params={"name": query},   # oder f"{query}%" für Prefix-Suche
    )
    if len(selectedLocation) == 0:
        st.error("Ort nicht gefunden")
    else:
        latitude = float(selectedLocation["latitude"][0])
        longitude = float(selectedLocation["longitude"][0])

        #cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
        #retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client() #(session=retry_session)

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": [
                "weather_code", "temperature_2m_max", "temperature_2m_min",
                "apparent_temperature_max", "apparent_temperature_min",
                "sunrise", "sunset", "daylight_duration", "sunshine_duration",
                "uv_index_max", "uv_index_clear_sky_max", "rain_sum", "showers_sum",
                "snowfall_sum", "precipitation_sum", "precipitation_hours",
                "precipitation_probability_max", "wind_speed_10m_max",
                "wind_gusts_10m_max", "shortwave_radiation_sum",
                "wind_direction_10m_dominant", "et0_fao_evapotranspiration"
            ],
            "hourly": [
                "temperature_2m", "relative_humidity_2m", "dew_point_2m",
                "apparent_temperature", "precipitation_probability", "precipitation",
                "rain", "showers", "snow_depth", "snowfall", "weather_code",
                "surface_pressure", "pressure_msl", "cloud_cover",
                "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high",
                "visibility", "evapotranspiration", "et0_fao_evapotranspiration",
                "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_80m",
                "wind_speed_120m", "wind_speed_180m", "wind_direction_10m",
                "wind_direction_80m", "wind_direction_120m", "wind_direction_180m",
                "wind_gusts_10m", "temperature_80m", "temperature_120m",
                "temperature_180m", "soil_temperature_0cm", "soil_temperature_6cm",
                "soil_temperature_18cm", "soil_temperature_54cm",
                "soil_moisture_0_to_1cm", "soil_moisture_1_to_3cm",
                "soil_moisture_3_to_9cm", "soil_moisture_9_to_27cm",
                "soil_moisture_27_to_81cm"
            ],
            "current": [
                "temperature_2m", "relative_humidity_2m", "apparent_temperature",
                "is_day", "precipitation", "rain", "showers", "snowfall",
                "weather_code", "cloud_cover", "pressure_msl", "surface_pressure",
                "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"
            ],
            "timezone": "Europe/Berlin",
            "past_days": 14,
            "forecast_days": 14,
        }

        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        # ---------------- Current in Dict ----------------
        current = response.Current()  # Reihenfolge wie params["current"][web:160]

        cur = {
            "temperature_2m":       current.Variables(0).Value(),
            "relative_humidity_2m": current.Variables(1).Value(),
            "apparent_temperature": current.Variables(2).Value(),
            "is_day":               current.Variables(3).Value(),
            "precipitation":        current.Variables(4).Value(),
            "rain":                 current.Variables(5).Value(),
            "showers":              current.Variables(6).Value(),
            "snowfall":             current.Variables(7).Value(),
            "weather_code":         current.Variables(8).Value(),
            "cloud_cover":          current.Variables(9).Value(),
            "pressure_msl":         current.Variables(10).Value(),
            "surface_pressure":     current.Variables(11).Value(),
            "wind_speed_10m":       current.Variables(12).Value(),
            "wind_direction_10m":   current.Variables(13).Value(),
            "wind_gusts_10m":       current.Variables(14).Value(),
        }

        # ---------------- Hourly DataFrame ----------------
        hourly = response.Hourly()
        hourly_time = pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s"),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )

        hourly_df = pd.DataFrame({
            "time": hourly_time,
            "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
            "relative_humidity_2m": hourly.Variables(1).ValuesAsNumpy(),
            "apparent_temperature": hourly.Variables(3).ValuesAsNumpy(),
            "precipitation": hourly.Variables(5).ValuesAsNumpy(),
            "rain": hourly.Variables(6).ValuesAsNumpy(),
            "showers": hourly.Variables(7).ValuesAsNumpy(),
            "snowfall": hourly.Variables(9).ValuesAsNumpy(),
            "weather_code": hourly.Variables(10).ValuesAsNumpy(),
            "cloud_cover": hourly.Variables(13).ValuesAsNumpy(),
            "wind_speed_10m": hourly.Variables(22).ValuesAsNumpy(),
            "wind_direction_10m": hourly.Variables(28).ValuesAsNumpy(),
            "wind_gusts_10m": hourly.Variables(31).ValuesAsNumpy(),
        })

        # ---------------- Daily DataFrame (14 zurück + 14 vor) ----------------
        daily = response.Daily()
        daily_time = pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s"),
            end=pd.to_datetime(daily.TimeEnd(), unit="s"),
            freq=pd.Timedelta(days=1),
            inclusive="left",
        )

        daily_df = pd.DataFrame({
            "date": daily_time,
            "weather_code": daily.Variables(0).ValuesAsNumpy(),
            "temperature_2m_max": daily.Variables(1).ValuesAsNumpy(),
            "temperature_2m_min": daily.Variables(2).ValuesAsNumpy(),
            "apparent_temperature_max": daily.Variables(3).ValuesAsNumpy(),
            "apparent_temperature_min": daily.Variables(4).ValuesAsNumpy(),
            "rain_sum": daily.Variables(11).ValuesAsNumpy(),
            "precipitation_sum": daily.Variables(14).ValuesAsNumpy(),
            "wind_speed_10m_max": daily.Variables(18).ValuesAsNumpy(),
            "wind_gusts_10m_max": daily.Variables(19).ValuesAsNumpy(),
        })



with col2:
    query_button = st.button("Suchen")

with col3:
    st.write("")



# Minimale Optionen: Monatsansicht + klickbare Tage
calendar_options = {
    "initialView": "dayGridMonth",  # Monatsansicht
    "selectable": True,             # Klick auf Datum / Bereich
}

# 2 Spalten: links breit (Wetter-Metrics), rechts schmal (Kalender + Metric)
col1, col2 = st.columns([2, 1], border=True, gap="small")

# ---- linke Spalte: mehrere Metrics in Unter-Spalten ----
with col1:
    if cur is not None:
        box = st.container(border=False)

        with box:
            m1, m2, m3 = st.columns(3, gap="small")  # „sub columns“ im Container

            with m1:
                st.metric("🌡️ Lufttemperatur", f"{cur['temperature_2m']:.1f} °C")
                st.metric("🥵 Gefühlte Temp.", f"{cur['apparent_temperature']:.1f} °C")

            with m2:
                st.metric("💧 rel. Feuchte", f"{cur['relative_humidity_2m']:.0f} %")
                st.metric("☁️ Bewölkung", f"{cur['cloud_cover']:.0f} %")

            with m3:
                st.metric("🌬️ Wind 10 m", f"{cur['wind_speed_10m']:.1f} km/h")
                st.metric("💨 Böen 10 m", f"{cur['wind_gusts_10m']:.1f} km/h")

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
        if cur is not None:
            st.metric("🌧️ Niederschlag", f"{cur['precipitation']:.1f} mm")



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