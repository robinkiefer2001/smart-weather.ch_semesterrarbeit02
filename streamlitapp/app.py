import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from api_client import fetch_weather_data
from map_handler import display_weather_map, fetch_city_weather_data
from database import search_location

# ===== DEUTSCHE TAGE UND MONATE =====
DEUTSCH_TAGE = {
    0: 'Montag', 1: 'Dienstag', 2: 'Mittwoch', 3: 'Donnerstag',
    4: 'Freitag', 5: 'Samstag', 6: 'Sonntag'
}
DEUTSCH_TAGE_KURZ = {
    0: 'Mo', 1: 'Di', 2: 'Mi', 3: 'Do',
    4: 'Fr', 5: 'Sa', 6: 'So'
}
DEUTSCH_MONATE = {
    1: 'Januar', 2: 'Februar', 3: 'März', 4: 'April',
    5: 'Mai', 6: 'Juni', 7: 'Juli', 8: 'August',
    9: 'September', 10: 'Oktober', 11: 'November', 12: 'Dezember'
}

def format_date_german(date_obj, format_type='long'):
    """Formatiere Datum auf Deutsch.
    format_type: 'long' (Montag, 05.01.2026), 'short' (Mo, 05.01), 'long_full' (Montag, 05. Januar 2026)
    """
    weekday = DEUTSCH_TAGE if format_type != 'short' else DEUTSCH_TAGE_KURZ
    day_name = weekday[date_obj.weekday()]
    
    if format_type == 'long':
        return f"{day_name}, {date_obj.strftime('%d.%m.%Y')}"
    elif format_type == 'short':
        return f"{day_name}\n{date_obj.strftime('%d.%m')}"
    elif format_type == 'long_full':
        month_name = DEUTSCH_MONATE[date_obj.month]
        return f"{day_name}, {date_obj.day}. {month_name} {date_obj.year}"
    return str(date_obj)
from data_handlers import (
    prepare_hourly_overview, prepare_temperature_chart, prepare_precipitation_chart,
    prepare_wind_chart, prepare_cloud_chart, prepare_snow_chart,
    calculate_temperature_stats, calculate_precipitation_stats,
    calculate_wind_stats, calculate_cloud_stats, calculate_snow_stats, weather_description, weather_icon
)
from ui_components import (
    display_current_metrics, display_hourly_overview, display_temperature_chart,
    display_precipitation_chart, display_wind_chart, display_cloud_chart, display_snow_chart,
    display_detailed_table
)

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="Smart Weather Switzerland",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== CUSTOM CSS =====
st.markdown("""
<style>
    .metric-card {
        padding: 16px;
        background: linear-gradient(135deg, #3b82f6 0%, #1e3a8a 100%);
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 2px 8px rgba(30, 58, 138, 0.15);
    }
    .day-card {
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid #d0d0d0;
    }
    .day-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    }
    .day-selected {
        border: 2px solid #3b82f6;
        background: #eff6ff !important;

    }
</style>
""", unsafe_allow_html=True)

# ===== SESSION STATE INITIALIZATION =====
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = None
if 'selected_location' not in st.session_state:
    st.session_state.selected_location = None
if 'selected_day_offset' not in st.session_state:
    st.session_state.selected_day_offset = 0
if 'cached_location_coords' not in st.session_state:
    st.session_state.cached_location_coords = None  # Caching: (latitude, longitude)
if 'map_data_cache' not in st.session_state:
    st.session_state.map_data_cache = None

# ===== INITIALIZATION AT START =====
if st.session_state.weather_data is None:
    with st.spinner("📡 Lade Wetterdaten für Schweiz..."):
        try:
            current_data, hourly_df, daily_df = fetch_weather_data(46.95, 7.45)
            st.session_state.weather_data = {
                'current': current_data,
                'hourly_df': hourly_df,
                'daily_df': daily_df
            }
        except Exception as e:
            st.warning(f"Konnte Wetterdaten nicht laden: {e}")

heute = datetime.now().date()

# ===== HEADER =====
st.title("🌤️ Smart Weather Switzerland")
st.markdown("Echtzeit Wettervorhersage mit interaktiver Karte und Tagesdetails")

# ===== NUR ZEIGEN WENN ORT AUSGEWÄHLT IST =====
if st.session_state.weather_data is None:
    st.info("📍 Bitte suchen Sie einen Ort aus der Karte um zu starten")

# ===== TABS: DRILL-DOWN KONZEPT =====
if st.session_state.weather_data is not None:
    tab_map, tab_calendar, tab_detail, tab_forecast = st.tabs(
        ["🗺️ Wetterkarte", "📅 Kalender & Woche", "📊 Tagesdetail", "🔮 14-Tage Prognose"]
    )
else:
    # Nur Kartentab wenn kein Ort ausgewählt
    tab_map = st.container()
    tab_calendar = None
    tab_detail = None
    tab_forecast = None

# ==================== TAB 1: WETTERKARTE ====================
with tab_map:
    st.subheader("🗺️ Interaktive Wetterkarte der Schweiz")
    
    # Such-Bereich
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        search_query = st.text_input(
            label="",
            placeholder="🔍 Ort suchen (z.B. 'Bern', 'Zürich', 'Genf')",
            key="location_search"
        )
    
    with search_col2:
        search_button = st.button("🔄 Suchen", use_container_width=True)
    
    if search_button and search_query:
        with st.spinner("📡 Suche Ort..."):
            search_results = search_location(search_query)
            if search_results:
                # search_results ist ein Tuple (latitude, longitude)
                latitude, longitude = search_results
                st.success(f"✅ Ort '{search_query}' gefunden!")
                st.session_state.selected_location = (search_query, latitude, longitude)
                
                # Prüfe Cache: nur neu laden wenn andere Koordinaten
                if st.session_state.cached_location_coords != (latitude, longitude):
                    try:
                        with st.spinner("📡 Lade Wetterdaten..."):
                            current_data, hourly_df, daily_df = fetch_weather_data(latitude, longitude)
                            st.session_state.weather_data = {
                                'current': current_data,
                                'hourly_df': hourly_df,
                                'daily_df': daily_df
                            }
                            st.session_state.cached_location_coords = (latitude, longitude)
                            st.session_state.selected_day_offset = 0
                    except Exception as e:
                        st.error(f"Fehler: {e}")
                else:
                    st.info("✅ Daten aus Cache geladen (keine neuen Anfragen)")
            else:
                st.warning(f"❌ Keine Ergebnisse für '{search_query}' gefunden.")
    
    # Karte anzeigen
    st.markdown("---")
    with st.container():
        with st.spinner("🗺️ Lade Wetterkarte..."):
            display_weather_map(show_loading=False, map_height=600)
    
    # Legende
    st.markdown("---")
    with st.expander("📝 Kartenlegende", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Temperaturfarben:**
            - 🔵 **Dunkelblau**: < -5°C (sehr kalt)
            - 🟦 **Blau**: -5 bis 0°C (kalt)
            - 🟩 **Grün**: 0-10°C (kühl)
            - 🟨 **Gelb**: 10-15°C (kühl-mild)
            - 🟧 **Orange**: 15-20°C (mild)
            - 🟥 **Rot**: > 20°C (warm)
            """)
        with col2:
            st.markdown("""
            **Wetter-Symbole:**
            - ☀️ Sonnig
            - 🌤️ Teilweise bewölkt
            - ⛅ Bewölkt
            - ☁️ Stark bewölkt
            - 🌫️ Nebel
            - 🌧️ Regen
            - ❄️ Schnee
            - ⛈️ Gewitter
            """)

# ==================== TAB 2: KALENDER & WOCHENÜBERSICHT ====================
if tab_calendar is not None:
    with tab_calendar:
        st.subheader("📅 7-Tage Kalender & Wochenübersicht")
        
        if st.session_state.weather_data is not None:
            daily_df = st.session_state.weather_data.get('daily_df')
            
            if daily_df is not None and not daily_df.empty:
                # Tage-Navigation
                nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])
                
                with nav_col1:
                    if st.button("⬅️ Vorheriger Tag", use_container_width=True):
                        st.session_state.selected_day_offset = max(0, st.session_state.selected_day_offset - 1)
                        st.rerun()
                
                with nav_col2:
                    selected_idx = st.session_state.selected_day_offset
                    if selected_idx < len(daily_df):
                        selected_date = daily_df.iloc[selected_idx]['date']
                        st.info(f"📍 Ausgewählter Tag: **{format_date_german(selected_date, 'long')}**", icon="📌")
                
                with nav_col3:
                    if st.button("Nächster Tag ➡️", use_container_width=True):
                        if st.session_state.selected_day_offset < len(daily_df) - 1:
                            st.session_state.selected_day_offset += 1
                            st.rerun()
                
                st.markdown("---")
                
                # 7-Tage Kalender mit Wetter-Symbolen
                st.write("**📅 Nächste 7 Tage:**")
                
                week_cols = st.columns(7)
                
                for idx, (col, (_, row)) in enumerate(zip(week_cols, daily_df.head(7).iterrows())):
                    with col:
                        date = row['date']
                        date_str = format_date_german(date, 'short')
                        temp_max = row.get('temperature_2m_max', '--')
                        temp_min = row.get('temperature_2m_min', '--')
                        precip = row.get('precipitation_sum', 0)
                        weather_code = int(row.get('weather_code', 0))
                        emoji = weather_icon(weather_code)
                        
                        # Fallback wenn emoji leer ist
                        if not emoji:
                            emoji = "🌤️"
                        
                        # Hintergrundfarbe je nach Temperatur (Blau-Weiss-Gelb Schema)
                        if isinstance(temp_max, (int, float)):
                            if temp_max < 0:
                                bg_color = "#eff6ff"  # Sehr helles Blau
                            elif temp_max < 5:
                                bg_color = "#f9fafb"  # Weiss-Grau
                            elif temp_max < 10:
                                bg_color = "#fffbeb"  # Sehr helles Gelb
                            elif temp_max < 15:
                                bg_color = "#fef9e7"  # Helles Gelb
                            else:
                                bg_color = "#fef3c7"  # Sanftes Gelb
                        else:
                            bg_color = "#f5f5f5"
                        
                        # Markiere ausgewählten Tag
                        border = "2px solid #3b82f6" if idx == st.session_state.selected_day_offset else "1px solid #e5e7eb"
                        
                        # Klickbare Karte für Tag
                        temp_max_str = str(temp_max) if isinstance(temp_max, str) else f'{temp_max:.2f}'
                        temp_min_str = str(temp_min) if isinstance(temp_min, str) else f'{temp_min:.2f}'
                        precip_str = f'{precip:.2f}'
                        
                        st.markdown(f"""
                        <div style="
                            background: {bg_color};
                            border: {border};
                            padding: 12px;
                            border-radius: 8px;
                            text-align: center;
                            cursor: pointer;
                            transition: all 0.3s ease;
                        ">
                            <small style="font-weight: bold;">{date_str}</small><br>
                            <div style="font-size: 32px; margin: 8px 0;">{emoji}</div>
                            <small><strong>↑ {temp_max_str}°</strong></small><br>
                            <small>↓ {temp_min_str}°</small><br>
                            <small>💧 {precip_str}mm</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("📌 Wählen", key=f"day_select_{idx}", use_container_width=True):
                            st.session_state.selected_day_offset = idx
                            st.rerun()
            else:
                st.warning("⚠️ Keine Wetterdaten für Kalender verfügbar.")
        else:
            st.warning("⚠️ Keine Wetterdaten verfügbar. Bitte auf der Kartenseite einen Ort suchen.")

# ==================== TAB 3: TAGESDETAIL ====================
if tab_detail is not None:
    with tab_detail:
        st.subheader("📊 Detailansicht des ausgewählten Tages")
        
        if st.session_state.weather_data is not None:
            daily_df = st.session_state.weather_data.get('daily_df')
            hourly_df = st.session_state.weather_data.get('hourly_df')
            
            if daily_df is not None and hourly_df is not None and not daily_df.empty:
                # Ausgewählten Tag holen
                selected_idx = min(st.session_state.selected_day_offset, len(daily_df) - 1)
                selected_row = daily_df.iloc[selected_idx]
                selected_date = selected_row['date']
                
                st.markdown(f"### {format_date_german(selected_date, 'long_full')}")
                
                # Detaillierte Metriken
                metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)
                
                with metric_col1:
                    max_temp = selected_row.get('temperature_2m_max', '--')
                    if isinstance(max_temp, (int, float)):
                        max_temp = f"{max_temp:.2f}"
                    st.metric("🌡️ Max Temperatur", f"{max_temp}°C")
                
                with metric_col2:
                    min_temp = selected_row.get('temperature_2m_min', '--')
                    if isinstance(min_temp, (int, float)):
                        min_temp = f"{min_temp:.2f}"
                    st.metric("❄️ Min Temperatur", f"{min_temp}°C")
                
                with metric_col3:
                    app_max_temp = selected_row.get('apparent_temperature_max', '--')
                    if isinstance(app_max_temp, (int, float)):
                        app_max_temp = f"{app_max_temp:.2f}"
                    st.metric("🌡️ Gefühlte Max", f"{app_max_temp}°C")
                
                with metric_col4:
                    app_min_temp = selected_row.get('apparent_temperature_min', '--')
                    if isinstance(app_min_temp, (int, float)):
                        app_min_temp = f"{app_min_temp:.2f}"
                    st.metric("❄️ Gefühlte Min", f"{app_min_temp}°C")
                
                with metric_col5:
                    sunshine = selected_row.get('sunshine_duration', '--')
                    if isinstance(sunshine, (int, float)):
                        sunshine = f"{sunshine:.2f}"
                    st.metric(
                        "☀️ Sonnenschein",
                        f"{sunshine}"
                    )
                
                st.markdown("---")
                
                # Stündliche Daten für diesen Tag
                hourly_df = st.session_state.weather_data.get('hourly_df')
                if hourly_df is not None:
                    daily_hourly = hourly_df[hourly_df['time'].dt.date == selected_date.date()].copy()
                    
                    if not daily_hourly.empty:
                        st.write("**⏰ Stündliche Vorhersage:**")
                        prepared_hourly = prepare_hourly_overview(daily_hourly, selected_date.date())
                        display_hourly_overview(prepared_hourly)
                
                st.markdown("---")
                
                # Grafiken in Tabs
                st.write("**📈 Diagramme & Verlauf:**")
                
                if hourly_df is not None:
                    # Prepare chart data für alle Charts (übergebe den gesamten hourly_df)
                    temp_chart_df = prepare_temperature_chart(hourly_df, selected_date.date())
                    precip_chart_df = prepare_precipitation_chart(hourly_df, selected_date.date())
                    wind_chart_df = prepare_wind_chart(hourly_df, selected_date.date())
                    cloud_chart_df = prepare_cloud_chart(hourly_df, selected_date.date())
                    snow_chart_df = prepare_snow_chart(hourly_df, selected_date.date())
                    
                    # Berechne Statistiken (übergebe den gesamten hourly_df)
                    temp_stats = calculate_temperature_stats(hourly_df, selected_date.date())
                    precip_stats = calculate_precipitation_stats(hourly_df, selected_date.date())
                    wind_stats = calculate_wind_stats(hourly_df, selected_date.date())
                    cloud_stats = calculate_cloud_stats(hourly_df, selected_date.date())
                    snow_stats = calculate_snow_stats(hourly_df, selected_date.date())
                    
                    # Tabs für Diagramme
                    tab_temp, tab_precip, tab_wind, tab_cloud, tab_snow = st.tabs([
                        "🌡️ Temperatur",
                        "💧 Niederschlag",
                        "💨 Wind",
                        "☁️ Bewölkung",
                        "❄️ Schnee"
                    ])
                    
                    with tab_temp:
                        st.subheader("🌡️ Temperaturverlauf")
                        display_temperature_chart(temp_chart_df, temp_stats)
                    
                    with tab_precip:
                        st.subheader("💧 Niederschlag & Feuchte")
                        display_precipitation_chart(precip_chart_df, precip_stats)
                    
                    with tab_wind:
                        st.subheader("💨 Windgeschwindigkeit")
                        display_wind_chart(wind_chart_df, wind_stats)
                    
                    with tab_cloud:
                        st.subheader("☁️ Wolkenbedeckung")
                        display_cloud_chart(cloud_chart_df, cloud_stats)
                    
                    with tab_snow:
                        st.subheader("❄️ Schneefall")
                        display_snow_chart(snow_chart_df, snow_stats)
                else:
                    st.warning("Stündliche Daten nicht verfügbar.")
            else:
                st.warning("⚠️ Keine detaillierten Daten für diesen Tag verfügbar.")
        else:
            st.warning("⚠️ Keine Wetterdaten verfügbar. Bitte auf der Kartenseite einen Ort suchen.")

# ==================== TAB 4: 14-TAGE PROGNOSE ====================
if tab_forecast is not None:
    with tab_forecast:
        st.subheader("🔮 14-Tage Wetterprognose")
        
        if st.session_state.weather_data is not None:
            daily_df = st.session_state.weather_data.get('daily_df')
            
            if daily_df is not None and not daily_df.empty:
                # Prognose-Tabelle
                forecast_display = daily_df.head(14).copy()
                forecast_display['Datum'] = forecast_display['date'].apply(lambda d: format_date_german(d, 'long'))
                
                # Wetter-Symbol und Beschreibung (aus data_handlers)
                forecast_display['Wetter'] = forecast_display['weather_code'].apply(
                    lambda code: f"{weather_icon(int(code))} {weather_description(int(code))}"
                )
                
                forecast_display['Max °C'] = forecast_display['temperature_2m_max'].round(2)
                forecast_display['Min °C'] = forecast_display['temperature_2m_min'].round(2)
                forecast_display['Niederschlag'] = forecast_display['precipitation_sum'].round(2).astype(str) + " mm"
                
                display_cols = ['Datum', 'Wetter', 'Max °C', 'Min °C', 'Niederschlag']
                
                st.dataframe(
                    forecast_display[display_cols],
                    use_container_width=True,
                    hide_index=True,
                    height=500
                )
            else:
                st.warning("⚠️ Keine Prognosedaten verfügbar.")
        else:
            st.warning("⚠️ Keine Wetterdaten verfügbar. Bitte auf der Kartenseite einen Ort suchen.")

# ===== FOOTER =====
st.markdown("---")

st.markdown("""
<div style="text-align: center; color: gray; font-size: 11px; margin-top: 20px;">
    <p>🌤️ Schulprojekt | Powered by Open-Meteo API & Streamlit</p>
    <p>Aktualisiert: {}</p>
    <p style="margin-top: 10px;">
        <a href="?page=1_Impressum" style="color: #3b82f6; text-decoration: none; cursor: pointer;">📋 Impressum</a> | 
        <a href="?page=2_Datenschutz" style="color: #3b82f6; text-decoration: none; cursor: pointer;">🔒 Datenschutz</a>
    </p>
</div>
""".format(datetime.now().strftime("%d.%m.%Y %H:%M:%S")), unsafe_allow_html=True)
