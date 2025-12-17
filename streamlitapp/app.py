import streamlit as st
import psycopg2
import psycopg
import datetime
import streamlit_calendar
import streamlit.components.v1 as components
import pandas as pd
from streamlit_calendar import calendar  # neues Package
from sqlalchemy import text
#import requests_cache
#from retry_requests import retry
import requests
import openmeteo_requests
from numpy.random import default_rng as rng

conn = st.connection("sql")
#cur = None

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

# einmalig initialisieren
if "weather_data" not in st.session_state:
    st.session_state.weather_data = None

if query_button and query:
    q = query.strip().replace("'", "''")

    selectedLocation = conn.query(
        f"""
        SELECT latitude, longitude
        FROM geo_location
        WHERE name ILIKE '%{q}%'
        LIMIT 1;
        """
    )

    st.write("Debug selectedLocation:", selectedLocation)  # zum Testen
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

        st.session_state.weather_data = {
        "cur": cur,
        "hourly_df": hourly_df,
        "daily_df": daily_df,
    }

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
    if st.session_state.weather_data is not None:
        box = st.container(border=False)

        with box:
            st.write("Wetterdaten für {datetime.date.today().strftime('%d.%m.%Y')}")
            m1, m2, m3 = st.columns(3, gap="small")  # „sub columns“ im Container

            with m1:
                st.metric("🌡️ Lufttemperatur", f"{st.session_state.weather_data['cur']['temperature_2m']:.1f} °C")
                st.metric("🥵 Gefühlte Temp.", f"{st.session_state.weather_data['cur']['apparent_temperature']:.1f} °C")

            with m2:
                st.metric("💧 rel. Feuchte", f"{st.session_state.weather_data['cur']['relative_humidity_2m']:.0f} %")
                st.metric("☁️ Bewölkung", f"{st.session_state.weather_data['cur']['cloud_cover']:.0f} %")

            with m3:
                st.metric("🌬️ Wind 10 m", f"{st.session_state.weather_data['cur']['wind_speed_10m']:.1f} km/h")
                st.metric("💨 Böen 10 m", f"{st.session_state.weather_data['cur']['wind_gusts_10m']:.1f} km/h")

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
        if st.session_state.weather_data is not None:
            st.metric("🌧️ Niederschlag", f"{st.session_state.weather_data['cur']['precipitation']:.1f} mm")


col1, col2 = st.columns([1, 1], gap="small")
with col1:
    if st.session_state.weather_data is not None:
        st.subheader("Stündliche Tagesübersicht")
        # Tagesübersicht (stündlich)    # Heute's Daten filtern
        Tagesübersicht = st.session_state.weather_data['hourly_df'][
            st.session_state.weather_data['hourly_df']['time'].dt.date == heute
        ].copy()
    
        # Für Anzeige formatieren
        display_df = Tagesübersicht[[
            "time", 
            "temperature_2m", 
            "apparent_temperature",
            "relative_humidity_2m", 
            "precipitation",
            "weather_code",
            "cloud_cover",
            "wind_speed_10m",
            "wind_gusts_10m",
            "wind_direction_10m"
        ]].copy()

        # Nach Zeit sortieren
        display_df = display_df.sort_values("time")
    
        # Spalten umbenennen für bessere Lesbarkeit
        display_df.columns = [
            "🕐 Uhrzeit",
            "🌡️ Temp. (°C)",
            "🥵 Gefühlt (°C)",
            "💧 Feuchte (%)",
            "🌧️ Niederschlag (mm)",
            "☁️ Wetter",
            "☁️ Bewölkung (%)",
            "🌬️ Wind (km/h)",
            "💨 Böen (km/h)",
            "➡️ Windrichtung (°)"
        ]
        
        # Zeit formatieren (nur Stunde anzeigen)
        display_df["🕐 Uhrzeit"] = display_df["🕐 Uhrzeit"].dt.strftime("%H:%M")
    
        # Dezimalzahlen formatieren
        display_df["🌡️ Temp. (°C)"] = display_df["🌡️ Temp. (°C)"].round(1)
        display_df["🥵 Gefühlt (°C)"] = display_df["🥵 Gefühlt (°C)"].round(1)
        display_df["💧 Feuchte (%)"] = display_df["💧 Feuchte (%)"].round(0).astype(int)
        display_df["🌧️ Niederschlag (mm)"] = display_df["🌧️ Niederschlag (mm)"].round(1)
        display_df["☁️ Bewölkung (%)"] = display_df["☁️ Bewölkung (%)"].round(0).astype(int)
        display_df["🌬️ Wind (km/h)"] = display_df["🌬️ Wind (km/h)"].round(1)
        display_df["💨 Böen (km/h)"] = display_df["💨 Böen (km/h)"].round(1)
        display_df["➡️ Windrichtung (°)"] = display_df["➡️ Windrichtung (°)"].round(0).astype(int)
    
        # Tabelle anzeigen
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "🕐 Uhrzeit": st.column_config.TextColumn(width="small"),
                "🌡️ Temp. (°C)": st.column_config.NumberColumn(width="small"),
                "🥵 Gefühlt (°C)": st.column_config.NumberColumn(width="small"),
                "💧 Feuchte (%)": st.column_config.NumberColumn(width="small"),
                "🌧️ Niederschlag (mm)": st.column_config.NumberColumn(width="small"),
                "☁️ Wetter": st.column_config.NumberColumn(width="small"),
                "☁️ Bewölkung (%)": st.column_config.NumberColumn(width="small"),
                "🌬️ Wind (km/h)": st.column_config.NumberColumn(width="small"),
                "💨 Böen (km/h)": st.column_config.NumberColumn(width="small"),
                "➡️ Windrichtung (°)": st.column_config.NumberColumn(width="small"),
            }
        )

with col2:
    st.subheader("Visuals")
    if st.session_state.weather_data is not None:
        # Temperaturveränderung berechnen (Differenz zur vorherigen Stunde)
        Tagesübersicht["temp_change"] = Tagesübersicht["temperature_2m"].diff()

        # Für die erste Stunde ist die Änderung NaN, das können wir mit 0 füllen
        Tagesübersicht["temp_change"] = Tagesübersicht["temp_change"].fillna(0)

        # Chart mit Original-Temperatur UND Veränderung
        st.line_chart(
            data=Tagesübersicht,
            x="time",
            y=["temperature_2m", "temp_change"],
            height=300,
            use_container_width=True,
        )
        # Optional: auch in der Tabelle anzeigen
        display_df["📈 Temp. Änderung (°C)"] = Tagesübersicht["temp_change"].round(2)


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