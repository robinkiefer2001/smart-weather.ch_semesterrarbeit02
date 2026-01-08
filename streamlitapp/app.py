import streamlit as st
import datetime
import streamlit.components.v1 as components
import pandas as pd
from streamlit_calendar import calendar
from api_client import fetch_weather_data
from database import search_location
from data_handlers import (
    weather_icon, weather_description,
    prepare_hourly_overview, prepare_table_display,
    prepare_temperature_chart, calculate_temperature_stats,
    prepare_precipitation_chart, calculate_precipitation_stats,
    prepare_wind_chart, calculate_wind_stats,
    prepare_cloud_chart, calculate_cloud_stats,
    prepare_snow_chart, calculate_snow_stats
)
from ui_components import (
    display_current_metrics, display_hourly_overview,
    display_detailed_table, display_temperature_chart,
    display_precipitation_chart, display_wind_chart,
    display_cloud_chart, display_snow_chart
)
from map_handler import display_weather_map

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
    location = search_location(query)
    
    if location is None:
        st.error("Ort nicht gefunden")
    else:
        latitude, longitude = location

        # API-Call über api_client.py
        current_data, hourly_df, daily_df = fetch_weather_data(latitude, longitude)

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
            
            display_current_metrics(st.session_state.weather_data['current'])
            
            col_houerlyOverview = st.container()
            with col_houerlyOverview:
                hourly_overview = prepare_hourly_overview(
                    st.session_state.weather_data['hourly_df'], heute
                )
                display_hourly_overview(hourly_overview)

# ---- RECHTE SPALTE: KALENDER + NIEDERSCHLAG ----
with metrics_col_right:
    cal_data = calendar(
        options={"initialView": "dayGridMonth", "selectable": True},
        key="smartweather_calendar",
    )

# ===== WETTER-KARTE MIT HAUPTSTÄDTEN =====
st.divider()
st.subheader("🗺️ Wetter-Übersicht der Schweiz")
st.write("Interaktive Karte mit aktuellen Temperaturen und Wetterbedingungen in den wichtigsten Schweizer Städten")

# Kartenlegende in einer ausziehbaren Spalte
with st.expander("📋 Kartenlegende anzeigen"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("""
        **Farbcodierung:**
        - ☀️ **Gold** = Sonnig
        - 🔵 **Blau** = Bewölkt
        - ⛅ **Grau** = Bedeckt
        """)
    
    with col2:
        st.write("""
        - 🌫️ **Dunkelgrau** = Nebel
        - 💧 **Royal Blau** = Regen
        - ❄️ **Hellblau** = Schnee
        """)
    
    with col3:
        st.write("""
        - 🔴 **Rot** = Gewitter
        
        **Interaktion:**
        - Klicke auf einen Ort für Details
        - Zoom und Pan mit Maus
        """)

# Karte in voller Breite
display_weather_map(show_loading=True, map_height=500)

# Refresh Button
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 8])
with col_btn1:
    if st.button("🔄 Karte aktualisieren", key="map_refresh"):
        st.rerun()

# ===== TABELLE + TEMPERATUR CHART =====
table_col, temp_chart_col = st.columns([1, 1], gap="small")

# ---- TABELLE: STÜNDLICHE ÜBERSICHT ----
with table_col:
    if st.session_state.weather_data is not None:
        table_display_df = prepare_table_display(
            st.session_state.weather_data['hourly_df'], heute
        )
        display_detailed_table(table_display_df)

# ---- TEMPERATUR CHART ----
with temp_chart_col:
    if st.session_state.weather_data is not None:
        temp_chart_df = prepare_temperature_chart(
            st.session_state.weather_data['hourly_df'], heute
        )
        temp_stats = calculate_temperature_stats(
            st.session_state.weather_data['hourly_df'], heute
        )
        display_temperature_chart(temp_chart_df, temp_stats)

# ===== NIEDERSCHLAG + WIND CHARTS =====
precip_wind_col_left, precip_wind_col_right = st.columns([1, 1], gap="small")

if st.session_state.weather_data is not None:
    # ---- NIEDERSCHLAG (LINKS) ----
    with precip_wind_col_left:
        precip_chart_df = prepare_precipitation_chart(
            st.session_state.weather_data['hourly_df'], heute
        )
        precip_stats = calculate_precipitation_stats(
            st.session_state.weather_data['hourly_df'], heute
        )
        display_precipitation_chart(precip_chart_df, precip_stats)
    
    # ---- WIND (RECHTS) ----
    with precip_wind_col_right:
        wind_chart_df = prepare_wind_chart(
            st.session_state.weather_data['hourly_df'], heute
        )
        wind_stats = calculate_wind_stats(
            st.session_state.weather_data['hourly_df'], heute
        )
        display_wind_chart(wind_chart_df, wind_stats)

# ===== BEWÖLKUNG + SCHNEEFALL CHARTS =====
cloud_snow_col_left, cloud_snow_col_right = st.columns([1, 1], gap="small")

if st.session_state.weather_data is not None:
    # ---- BEWÖLKUNG (LINKS) ----
    with cloud_snow_col_left:
        cloud_chart_df = prepare_cloud_chart(
            st.session_state.weather_data['hourly_df'], heute
        )
        cloud_stats = calculate_cloud_stats(
            st.session_state.weather_data['hourly_df'], heute
        )
        display_cloud_chart(cloud_chart_df, cloud_stats)

    # ---- SCHNEEFALL (RECHTS) ----
    with cloud_snow_col_right:
        snow_chart_df = prepare_snow_chart(
            st.session_state.weather_data['hourly_df'], heute
        )
        snow_stats = calculate_snow_stats(
            st.session_state.weather_data['hourly_df'], heute
        )
        display_snow_chart(snow_chart_df, snow_stats)


