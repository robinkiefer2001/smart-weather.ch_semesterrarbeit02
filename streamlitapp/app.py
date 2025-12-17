import streamlit as st
import psycopg2
import psycopg
import datetime
import streamlit_calendar
import streamlit.components.v1 as components
import pandas as pd
from streamlit_calendar import calendar
from sqlalchemy import text
import requests
import openmeteo_requests
from numpy.random import default_rng as rng

conn = st.connection("sql")

# ===== VARIABLEN =====
heute = datetime.date.today()

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="smart weather CH",
    page_icon="🌤️",
    layout="wide"
)

st.title("Smart Weather CH", anchor=False)
st.subheader("Wilkommen zur Smart Weather CH – Ihre persönliche Wetterquelle")

# ===== SESSION STATE INIT =====
if "weather_data" not in st.session_state:
    st.session_state.weather_data = None

# ===== SUCHBEREICH =====
search_col_left, search_col_middle, search_col_right = st.columns([2, 1, 2])

with search_col_left:
    query = st.text_input(
        "Suche",
        placeholder="Suchbegriff...",
        label_visibility="collapsed"
    )

with search_col_middle:
    query_button = st.button("Suchen")

with search_col_right:
    st.write("")

# ===== API CALL bei Button =====
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

    st.write("Debug selectedLocation:", selectedLocation)
    
    if len(selectedLocation) == 0:
        st.error("Ort nicht gefunden")
    else:
        latitude = float(selectedLocation["latitude"][0])
        longitude = float(selectedLocation["longitude"][0])

        openmeteo = openmeteo_requests.Client()

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

        # ===== CURRENT DATA =====
        current = response.Current()
        current_data = {
            "temperature_2m": current.Variables(0).Value(),
            "relative_humidity_2m": current.Variables(1).Value(),
            "apparent_temperature": current.Variables(2).Value(),
            "is_day": current.Variables(3).Value(),
            "precipitation": current.Variables(4).Value(),
            "rain": current.Variables(5).Value(),
            "showers": current.Variables(6).Value(),
            "snowfall": current.Variables(7).Value(),
            "weather_code": current.Variables(8).Value(),
            "cloud_cover": current.Variables(9).Value(),
            "pressure_msl": current.Variables(10).Value(),
            "surface_pressure": current.Variables(11).Value(),
            "wind_speed_10m": current.Variables(12).Value(),
            "wind_direction_10m": current.Variables(13).Value(),
            "wind_gusts_10m": current.Variables(14).Value(),
        }

        # ===== HOURLY DATA =====
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

        # ===== DAILY DATA =====
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

        # ===== IN SESSION SPEICHERN =====
        st.session_state.weather_data = {
            "current": current_data,
            "hourly_df": hourly_df,
            "daily_df": daily_df,
        }

# ===== HAUPTBEREICH: METRIKEN + KALENDER =====
metrics_col_left, metrics_col_right = st.columns([2, 1], border=True, gap="small")

# ---- LINKE SPALTE: AKTUELLE METRIKEN ----
with metrics_col_left:
    if st.session_state.weather_data is not None:
        metrics_box = st.container(border=False)

        with metrics_box:
            st.write(f"Wetterdaten für {heute.strftime('%d.%m.%Y')}")
            
            metric_col_temp, metric_col_humidity, metric_col_wind = st.columns(3, gap="small")

            with metric_col_temp:
                st.metric("🌡️ Lufttemperatur", 
                         f"{st.session_state.weather_data['current']['temperature_2m']:.1f} °C")
                st.metric("🥵 Gefühlte Temp.", 
                         f"{st.session_state.weather_data['current']['apparent_temperature']:.1f} °C")

            with metric_col_humidity:
                st.metric("💧 rel. Feuchte", 
                         f"{st.session_state.weather_data['current']['relative_humidity_2m']:.0f} %")
                st.metric("☁️ Bewölkung", 
                         f"{st.session_state.weather_data['current']['cloud_cover']:.0f} %")

            with metric_col_wind:
                st.metric("🌬️ Wind 10 m", 
                         f"{st.session_state.weather_data['current']['wind_speed_10m']:.1f} km/h")
                st.metric("💨 Böen 10 m", 
                         f"{st.session_state.weather_data['current']['wind_gusts_10m']:.1f} km/h")

# ---- RECHTE SPALTE: KALENDER + NIEDERSCHLAG ----
with metrics_col_right:
    cal_data = calendar(
        options={"initialView": "dayGridMonth", "selectable": True},
        key="smartweather_calendar",
    )

# ===== TABELLE + TEMPERATUR CHART =====
table_col, temp_chart_col = st.columns([1, 1], gap="small")

# ---- TABELLE: STÜNDLICHE ÜBERSICHT ----
with table_col:
    if st.session_state.weather_data is not None:
        st.subheader("📊 Stündliche Tagesübersicht")
        
        today_hourly_df = st.session_state.weather_data['hourly_df'][
            st.session_state.weather_data['hourly_df']['time'].dt.date == heute
        ].copy().sort_values("time")
        
        table_display_df = today_hourly_df[[
            "time", "temperature_2m", "apparent_temperature",
            "relative_humidity_2m", "precipitation",
            "cloud_cover", "wind_speed_10m", "wind_gusts_10m"
        ]].copy()

        table_display_df.columns = [
            "🕐 Uhrzeit", "🌡️ Temp. (°C)", "🥵 Gefühlt (°C)",
            "💧 Feuchte (%)", "🌧️ Niederschlag (mm)",
            "☁️ Bewölkung (%)", "🌬️ Wind (km/h)", "💨 Böen (km/h)"
        ]
        
        table_display_df["🕐 Uhrzeit"] = table_display_df["🕐 Uhrzeit"].dt.strftime("%H:%M")
        table_display_df["🌡️ Temp. (°C)"] = table_display_df["🌡️ Temp. (°C)"].round(1)
        table_display_df["🥵 Gefühlt (°C)"] = table_display_df["🥵 Gefühlt (°C)"].round(1)
        table_display_df["💧 Feuchte (%)"] = table_display_df["💧 Feuchte (%)"].round(0).astype(int)
        table_display_df["🌧️ Niederschlag (mm)"] = table_display_df["🌧️ Niederschlag (mm)"].round(1)
        table_display_df["☁️ Bewölkung (%)"] = table_display_df["☁️ Bewölkung (%)"].round(0).astype(int)
        table_display_df["🌬️ Wind (km/h)"] = table_display_df["🌬️ Wind (km/h)"].round(1)
        table_display_df["💨 Böen (km/h)"] = table_display_df["💨 Böen (km/h)"].round(1)
    
        st.dataframe(
            table_display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "🕐 Uhrzeit": st.column_config.TextColumn(width="small"),
                "🌡️ Temp. (°C)": st.column_config.NumberColumn(width="small"),
                "🥵 Gefühlt (°C)": st.column_config.NumberColumn(width="small"),
                "💧 Feuchte (%)": st.column_config.NumberColumn(width="small"),
                "🌧️ Niederschlag (mm)": st.column_config.NumberColumn(width="small"),
                "☁️ Bewölkung (%)": st.column_config.NumberColumn(width="small"),
                "🌬️ Wind (km/h)": st.column_config.NumberColumn(width="small"),
                "💨 Böen (km/h)": st.column_config.NumberColumn(width="small")
            }
        )

# ---- TEMPERATUR CHART ----
with temp_chart_col:
    if st.session_state.weather_data is not None:
        st.subheader("📈 Temperaturverlauf")
        
        today_hourly_df = st.session_state.weather_data['hourly_df'][
            st.session_state.weather_data['hourly_df']['time'].dt.date == heute
        ].copy().sort_values("time")

        today_hourly_df["temp_change"] = today_hourly_df["temperature_2m"].diff().fillna(0)

        temp_chart_df = today_hourly_df.copy()
        temp_chart_df["Uhrzeit"] = temp_chart_df["time"].dt.strftime("%H:00")
        temp_chart_df["Absolute Temperatur (°C)"] = temp_chart_df["temperature_2m"].round(1)
        temp_chart_df["Temperaturveränderung (°C)"] = temp_chart_df["temp_change"].round(2)

        st.line_chart(
            data=temp_chart_df.set_index("Uhrzeit")[
                ["Absolute Temperatur (°C)", "Temperaturveränderung (°C)"]
            ],
            height=400,
            use_container_width=True
        )

        max_temp = today_hourly_df["temperature_2m"].max()
        min_temp = today_hourly_df["temperature_2m"].min()
        max_increase = today_hourly_df["temp_change"].max()
        max_decrease = today_hourly_df["temp_change"].min()

        temp_metric_col1, temp_metric_col2, temp_metric_col3, temp_metric_col4 = st.columns(4)
        with temp_metric_col1:
            st.metric("🌡️ Max. Temperatur", f"{max_temp:.1f} °C")
        with temp_metric_col2:
            st.metric("🥶 Min. Temperatur", f"{min_temp:.1f} °C")
        with temp_metric_col3:
            st.metric("📈 Größter Anstieg", f"+{max_increase:.2f} °C/h")
        with temp_metric_col4:
            st.metric("📉 Größter Rückgang", f"{max_decrease:.2f} °C/h")

# ===== NIEDERSCHLAG + WIND CHARTS =====
precip_wind_col_left, precip_wind_col_right = st.columns([1, 1], gap="small")

if st.session_state.weather_data is not None:
    # ---- NIEDERSCHLAG (LINKS) ----
    with precip_wind_col_left:
        st.subheader("🌧️ Niederschlag")
        
        today_hourly_df = st.session_state.weather_data['hourly_df'][
            st.session_state.weather_data['hourly_df']['time'].dt.date == heute
        ].copy().sort_values("time")

        precip_chart_df = today_hourly_df.copy()
        precip_chart_df["Uhrzeit"] = precip_chart_df["time"].dt.strftime("%H:00")
        precip_chart_df["Regen (mm)"] = precip_chart_df["rain"].round(2)
        precip_chart_df["Schauer (mm)"] = precip_chart_df["showers"].round(2)

        st.line_chart(
            data=precip_chart_df.set_index("Uhrzeit")[
                ["Regen (mm)", "Schauer (mm)"]
            ],
            height=400,
            use_container_width=True
        )

        total_rain = today_hourly_df["rain"].sum()
        total_showers = today_hourly_df["showers"].sum()
        total_precipitation = total_rain + total_showers

        precip_metric_col1, precip_metric_col2, precip_metric_col3 = st.columns(3)
        with precip_metric_col1:
            st.metric("🌧️ Regen (gesamt)", f"{total_rain:.1f} mm")
        with precip_metric_col2:
            st.metric("⛈️ Schauer (gesamt)", f"{total_showers:.1f} mm")
        with precip_metric_col3:
            st.metric("💧 Gesamtniederschlag", f"{total_precipitation:.1f} mm")
    
    # ---- WIND (RECHTS) ----
    with precip_wind_col_right:
        st.subheader("🌬️ Wind")
        
        wind_chart_df = today_hourly_df.copy()
        wind_chart_df["Uhrzeit"] = wind_chart_df["time"].dt.strftime("%H:00")
        wind_chart_df["Wind (km/h)"] = wind_chart_df["wind_speed_10m"].round(1)
        wind_chart_df["Böen (km/h)"] = wind_chart_df["wind_gusts_10m"].round(1)

        st.line_chart(
            data=wind_chart_df.set_index("Uhrzeit")[
                ["Wind (km/h)", "Böen (km/h)"]
            ],
            height=400,
            use_container_width=True
        )

        max_wind = today_hourly_df["wind_speed_10m"].max()
        max_gusts = today_hourly_df["wind_gusts_10m"].max()

        wind_metric_col1, wind_metric_col2 = st.columns(2)
        with wind_metric_col1:
            st.metric("🌬️ Max. Wind", f"{max_wind:.1f} km/h")
        with wind_metric_col2:
            st.metric("💨 Max. Böen", f"{max_gusts:.1f} km/h")

# ===== BEWÖLKUNG + SCHNEEFALL CHARTS =====
cloud_snow_col_left, cloud_snow_col_right = st.columns([1, 1], gap="small")

if st.session_state.weather_data is not None:
    # ---- BEWÖLKUNG (LINKS) ----
    with cloud_snow_col_left:
        st.subheader("☁️ Bewölkung")
        
        cloud_chart_df = today_hourly_df.copy()
        cloud_chart_df["Uhrzeit"] = cloud_chart_df["time"].dt.strftime("%H:00")
        cloud_chart_df["Bewölkung (%)"] = cloud_chart_df["cloud_cover"].round(0).astype(int)

        st.line_chart(
            data=cloud_chart_df.set_index("Uhrzeit")[
                ["Bewölkung (%)"]
            ],
            height=400,
            use_container_width=True
        )

        avg_cloud_cover = today_hourly_df["cloud_cover"].mean()
        st.metric("☁️ Durchschnittl. Bewölkung", f"{avg_cloud_cover:.0f} %")

    # ---- SCHNEEFALL (RECHTS) ----
    with cloud_snow_col_right:
        st.subheader("❄️ Schneefall")
        
        snow_chart_df = today_hourly_df.copy()
        snow_chart_df["Uhrzeit"] = snow_chart_df["time"].dt.strftime("%H:00")
        snow_chart_df["Schneefall (cm)"] = snow_chart_df["snowfall"].round(2)

        st.line_chart(
            data=snow_chart_df.set_index("Uhrzeit")[
                ["Schneefall (cm)"]
            ],
            height=400,
            use_container_width=True
        )

        total_snowfall = today_hourly_df["snowfall"].sum()
        st.metric("❄️ Gesamtschneefall", f"{total_snowfall:.1f} cm")


#col1, col2 = st.columns([1, 2], border=True, gap="small")
#with col1:
#    st.write(
#        "Am Morgen in den Niederungen gebietsweise Nebel oder "
#        "Tieflagenbewölkung, lokal auch Hochnebel. Im Laufe des "
#        "Vormittags allmähliche Auflösung. Tagsüber meist sonnig mit "
#        "einzelnen hohen Wolkenfeldern. In den Alpen stellenweise "
#        "Föhnwolken. Am Nachmittag im Westen und Süden vermehrt "
#        "hochreichende Wolkenfelder. Temperatur am Nachmittag um 20 "
#        "Grad im Flachland, in den Bergen auf 2000 Metern um 8 Grad. "
#        "In den Alpen mässiger bis starker Föhnwind, sonst meist "
#        "leichter bis mässiger Wind aus Südwest bis West."
#    )
#with col2:
#    leaflet_html = """
#    <div id="map" style="width: 100%; height: 650px;"></div>
#
#    <!-- Leaflet CSS & JS -->
#    <link
#      rel="stylesheet"
#      href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
#    />
#    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
#
#    <script>
#      // Bounds für Schweiz‑Ausschnitt
#      var bounds = L.latLngBounds(
#        L.latLng(45.5, 5.5),   // Süd‑West
#        L.latLng(48.0, 11.0)   // Nord‑Ost
#      );
#
#      // Karte auf diese Bounds zoomen und begrenzen
#      var map = L.map('map', {
#        maxBounds: bounds,
#        maxBoundsViscosity: 1.0
#      }).fitBounds(bounds);
#
#      // Basiskarte (OSM)
#      L.tileLayer(
#        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
#        {
#          maxZoom: 14,
#          minZoom: 6
#        }
#      ).addTo(map);
#
#      // Optional: nur Rahmen statt blauem Overlay
#      L.rectangle(bounds, {
#        color: "#00aaff",
#        weight: 1,
#        fillOpacity: 0.0     // 0 = kein Blau, nur Linie
#      }).addTo(map);
#
#      // Später kannst du hier deine Meteo‑Daten als Layer hinzufügen,
#      // z.B. L.imageOverlay(imageUrl, bounds, {opacity: 0.6}).addTo(map);
#    </script>
#    """
#
#    components.html(leaflet_html, height=700)
#