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
if 'calendar_week_offset' not in st.session_state:
    st.session_state.calendar_week_offset = 0  # Wochennavigation
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
            # Setze selected_day_offset auf heutigen Tag
            today = pd.Timestamp.now().normalize()
            today_idx = 0
            for idx, row in daily_df.iterrows():
                if pd.to_datetime(row['date']).normalize() == today:
                    today_idx = idx
                    break
            st.session_state.selected_day_offset = today_idx
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
# Nur Tabs erstellen wenn Ort ausgewählt ist
if st.session_state.weather_data is not None:
    tab_map, tab_calendar, tab_detail, tab_forecast = st.tabs(
        ["🗺️ Wetterkarte", "📅 Kalender & Woche", "📊 Tagesdetail", "🔮 14-Tage Prognose"]
    )

# ==================== TAB 1: WETTERKARTE ====================
if st.session_state.weather_data is not None:
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
                            # Setze selected_day_offset auf heutigen Tag
                            today = pd.Timestamp.now().normalize()
                            today_idx = 0
                            for idx, row in daily_df.iterrows():
                                if pd.to_datetime(row['date']).normalize() == today:
                                    today_idx = idx
                                    break
                            st.session_state.selected_day_offset = today_idx
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
else:
    st.info("📍 Bitte suchen Sie einen Ort aus der Karte um zu starten")

# ==================== TAB 2: KALENDER & WOCHENÜBERSICHT ====================
if tab_calendar is not None:
    with tab_calendar:
        st.subheader("📅 Kalender & Wochenübersicht")
        
        if st.session_state.weather_data is not None:
            daily_df = st.session_state.weather_data.get('daily_df')
            
            if daily_df is not None and not daily_df.empty:
                # Aktuelles Datum bestimmen
                today = pd.Timestamp.now().date()
                
                # Finde Montag der aktuellen Woche
                today_pd = pd.Timestamp(today)
                monday_of_week = today_pd - pd.Timedelta(days=today_pd.weekday())
                
                # Berechne Startdatum für Anzeige (7 Tage vor Montag der aktuellen Woche)
                # Damit die aktuelle Woche vollständig in historischen Daten vorhanden ist
                display_start_date = monday_of_week - pd.Timedelta(days=7)
                
                # Kalender-Navigation
                nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])
                
                with nav_col1:
                    if st.button("⬅️ Vorherige Woche", use_container_width=True):
                        st.session_state.calendar_week_offset = max(-2, st.session_state.calendar_week_offset - 1)
                        st.rerun()
                
                with nav_col2:
                    # Zeige welche Woche aktuell angezeigt wird
                    week_start = monday_of_week + pd.Timedelta(days=st.session_state.calendar_week_offset * 7)
                    week_end = week_start + pd.Timedelta(days=6)
                    st.info(f"📍 Woche: **{format_date_german(week_start.to_pydatetime().date(), 'short').split(chr(10))[1]}** - **{format_date_german(week_end.to_pydatetime().date(), 'short').split(chr(10))[1]}**", icon="📌")
                
                with nav_col3:
                    if st.button("Nächste Woche ➡️", use_container_width=True):
                        st.session_state.calendar_week_offset = min(2, st.session_state.calendar_week_offset + 1)
                        st.rerun()
                
                st.markdown("---")
                
                # 7-Tage Kalender (Montag bis Sonntag)
                st.write("**📅 Woche:**")
                
                week_start_date = monday_of_week + pd.Timedelta(days=st.session_state.calendar_week_offset * 7)
                week_cols = st.columns(7)
                
                for day_offset in range(7):
                    current_date = (week_start_date + pd.Timedelta(days=day_offset)).to_pydatetime().date()
                    col = week_cols[day_offset]
                    
                    # Suche Daten für diesen Tag
                    matching_rows = daily_df[pd.to_datetime(daily_df['date']).dt.date == current_date]
                    
                    if not matching_rows.empty:
                        row = matching_rows.iloc[0]
                    else:
                        # Wenn keine Daten, skip
                        with col:
                            st.markdown(f"<div style='text-align: center; padding: 12px; color: #999;'>{format_date_german(current_date, 'short')}<br>Keine Daten</div>", unsafe_allow_html=True)
                        continue
                    
                    with col:
                        date_str = format_date_german(current_date, 'short')
                        temp_max = row.get('temperature_2m_max', '--')
                        temp_min = row.get('temperature_2m_min', '--')
                        precip = row.get('precipitation_sum', 0)
                        weather_code = int(row.get('weather_code', 0))
                        emoji = weather_icon(weather_code)
                        
                        if not emoji:
                            emoji = "🌤️"
                        
                        # Hintergrundfarbe
                        if isinstance(temp_max, (int, float)):
                            if temp_max < 0:
                                bg_color = "#eff6ff"
                            elif temp_max < 5:
                                bg_color = "#f9fafb"
                            elif temp_max < 10:
                                bg_color = "#fffbeb"
                            elif temp_max < 15:
                                bg_color = "#fef9e7"
                            else:
                                bg_color = "#fef3c7"
                        else:
                            bg_color = "#f5f5f5"
                        
                        # Markiere heutigen Tag und mache ihn größer
                        is_today = current_date == today
                        if is_today:
                            border = "3px solid #dc2626"
                            font_size = "36px"
                            padding = "16px"
                            font_weight_emoji = "bold"
                        else:
                            border = "1px solid #e5e7eb"
                            font_size = "28px"
                            padding = "12px"
                            font_weight_emoji = "normal"
                        
                        temp_max_str = str(temp_max) if isinstance(temp_max, str) else f'{temp_max:.2f}'
                        temp_min_str = str(temp_min) if isinstance(temp_min, str) else f'{temp_min:.2f}'
                        precip_str = f'{precip:.2f}'
                        
                        st.markdown(f"""
                        <div style="
                            background: {bg_color};
                            border: {border};
                            padding: {padding};
                            border-radius: 8px;
                            text-align: center;
                            cursor: pointer;
                            transition: all 0.3s ease;
                        ">
                            <small style="font-weight: bold;">{date_str}</small><br>
                            <div style="font-size: {font_size}; margin: 8px 0; font-weight: {font_weight_emoji};">{emoji}</div>
                            <small><strong>↑ {temp_max_str}°</strong></small><br>
                            <small>↓ {temp_min_str}°</small><br>
                            <small>💧 {precip_str}mm</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("📌 Wählen", key=f"day_select_{current_date}", use_container_width=True):
                            st.session_state.selected_day_offset = len(daily_df[pd.to_datetime(daily_df['date']).dt.date <= current_date]) - 1
                            st.rerun()
                
                st.markdown("---")
                
                # Wochengrafiken
                st.write("**📈 Entwicklung in der Woche:**")
                
                # Hole die Daten für die aktuelle Woche
                week_start_date = monday_of_week + pd.Timedelta(days=st.session_state.calendar_week_offset * 7)
                week_end_date = week_start_date + pd.Timedelta(days=6)
                
                week_data = daily_df[
                    (pd.to_datetime(daily_df['date']).dt.date >= week_start_date.date()) &
                    (pd.to_datetime(daily_df['date']).dt.date <= week_end_date.date())
                ].copy().reset_index(drop=True)
                
                if not week_data.empty:
                    # Vorbereitung der Wochendaten für Charts
                    week_data['date_str'] = pd.to_datetime(week_data['date']).apply(lambda d: format_date_german(d, 'short').split('\n')[0])
                    
                    # Tabs für Diagramme
                    tab_week_temp, tab_week_precip, tab_week_wind, tab_week_cloud, tab_week_snow = st.tabs([
                        "🌡️ Temperatur",
                        "💧 Niederschlag",
                        "💨 Wind",
                        "☁️ Bewölkung",
                        "❄️ Schnee"
                    ])
                    
                    with tab_week_temp:
                        st.subheader("🌡️ Temperaturverlauf über die Woche")
                        temp_cols = ['date_str', 'temperature_2m_max', 'temperature_2m_min', 'apparent_temperature_max', 'apparent_temperature_min']
                        if all(col in week_data.columns for col in temp_cols):
                            temp_week = week_data[temp_cols].copy()
                            temp_week.columns = ['Tag', 'Max Temp', 'Min Temp', 'Gefühlte Max', 'Gefühlte Min']
                            
                            import altair as alt
                            
                            # Umwandle in long format für Legende
                            temp_week_long = temp_week.melt(id_vars=['Tag'], var_name='Metrik', value_name='Temperatur')
                            
                            # Color und Dash-Mapping
                            color_scale = alt.Scale(domain=['Max Temp', 'Min Temp', 'Gefühlte Max', 'Gefühlte Min'],
                                                    range=['#dc2626', '#3b82f6', '#f97316', '#06b6d4'])
                            
                            # Dash-Pattern für gefühlte Temperaturen
                            stroke_dash_scale = alt.Scale(domain=['Max Temp', 'Min Temp', 'Gefühlte Max', 'Gefühlte Min'],
                                                          range=[[], [], [5, 5], [5, 5]])
                            
                            chart = alt.Chart(temp_week_long).mark_line(point=True, size=2).encode(
                                x=alt.X('Tag', sort=None),
                                y=alt.Y('Temperatur', scale=alt.Scale(zero=False), title='Temperatur (°C)'),
                                color=alt.Color('Metrik', scale=color_scale, legend=alt.Legend(title='Legende')),
                                strokeDash=alt.StrokeDash('Metrik', scale=stroke_dash_scale, legend=None)
                            ).properties(height=400).interactive()
                            st.altair_chart(chart, use_container_width=True)
                            st.dataframe(temp_week, use_container_width=True, hide_index=True)
                        else:
                            st.info("⚠️ Temperaturdaten nicht verfügbar")
                    
                    with tab_week_precip:
                        st.subheader("💧 Niederschlag über die Woche")
                        if 'precipitation_sum' in week_data.columns:
                            precip_week = week_data[['date_str', 'precipitation_sum']].copy()
                            precip_week.columns = ['Tag', 'Niederschlag (mm)']
                            
                            chart = alt.Chart(precip_week).mark_bar(color='#06b6d4').encode(
                                x=alt.X('Tag', sort=None),
                                y=alt.Y('Niederschlag (mm)')
                            ).properties(height=400).interactive()
                            
                            st.altair_chart(chart, use_container_width=True)
                            st.dataframe(precip_week, use_container_width=True, hide_index=True)
                        else:
                            st.info("⚠️ Niederschlagsdaten nicht verfügbar")
                    
                    with tab_week_wind:
                        st.subheader("💨 Windgeschwindigkeit über die Woche")
                        # Prüfe ob wind-Spalten existieren
                        if 'wind_speed_10m_max' in week_data.columns and 'wind_gusts_10m_max' in week_data.columns:
                            wind_week = week_data[['date_str', 'wind_speed_10m_max', 'wind_gusts_10m_max']].copy()
                            wind_week.columns = ['Tag', 'Max Windspeed (km/h)', 'Max Windböen (km/h)']
                            
                            # Umwandle in long format für Legende
                            wind_week_long = wind_week.melt(id_vars=['Tag'], var_name='Metrik', value_name='Windgeschwindigkeit')
                            
                            color_scale = alt.Scale(domain=['Max Windspeed (km/h)', 'Max Windböen (km/h)'],
                                                    range=['#10b981', '#ef4444'])
                            stroke_dash_scale = alt.Scale(domain=['Max Windspeed (km/h)', 'Max Windböen (km/h)'],
                                                          range=[[], [5, 5]])
                            
                            chart = alt.Chart(wind_week_long).mark_line(point=True, size=2).encode(
                                x=alt.X('Tag', sort=None),
                                y=alt.Y('Windgeschwindigkeit', scale=alt.Scale(zero=False), title='Windgeschwindigkeit (km/h)'),
                                color=alt.Color('Metrik', scale=color_scale, legend=alt.Legend(title='Legende')),
                                strokeDash=alt.StrokeDash('Metrik', scale=stroke_dash_scale, legend=None)
                            ).properties(height=400).interactive()
                            st.altair_chart(chart, use_container_width=True)
                            st.dataframe(wind_week, use_container_width=True, hide_index=True)
                        else:
                            st.info("⚠️ Windgeschwindigkeitsdaten nicht verfügbar")
                    
                    with tab_week_cloud:
                        st.subheader("☁️ Wolkenbedeckung über die Woche")
                        cloud_week = week_data[['date_str', 'cloud_cover']].copy() if 'cloud_cover' in week_data.columns else pd.DataFrame()
                        
                        if not cloud_week.empty:
                            cloud_week.columns = ['Tag', 'Wolkenbedeckung (%)']
                            
                            chart = alt.Chart(cloud_week).mark_bar(color='#94a3b8').encode(
                                x=alt.X('Tag', sort=None),
                                y=alt.Y('Wolkenbedeckung (%)', scale=alt.Scale(domain=[0, 100]))
                            ).properties(height=400)
                            
                            st.altair_chart(chart, use_container_width=True)
                            st.dataframe(cloud_week, use_container_width=True, hide_index=True)
                        else:
                            st.info("Keine Wolkendaten verfügbar")
                    
                    with tab_week_snow:
                        st.subheader("❄️ Schneefall über die Woche")
                        snow_week = week_data[['date_str', 'snowfall_sum']].copy() if 'snowfall_sum' in week_data.columns else pd.DataFrame()
                        
                        if not snow_week.empty:
                            snow_week.columns = ['Tag', 'Schneefall (cm)']
                            
                            chart = alt.Chart(snow_week).mark_bar(color='#7dd3fc').encode(
                                x=alt.X('Tag', sort=None),
                                y=alt.Y('Schneefall (cm)')
                            ).properties(height=400)
                            
                            st.altair_chart(chart, use_container_width=True)
                            st.dataframe(snow_week, use_container_width=True, hide_index=True)
                        else:
                            st.info("Keine Schneefalldaten verfügbar")
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
                        # Konvertiere von Sekunden zu Stunden
                        sunshine_hours = sunshine / 3600
                        sunshine = f"{sunshine_hours:.1f} h"
                    else:
                        sunshine = "--"
                    st.metric(
                        "☀️ Sonnenschein",
                        sunshine
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
                # Prognose-Tabelle: 7 Tage zurück + 14 Tage nach vorne
                daily_df_temp = daily_df.copy()
                daily_df_temp['date'] = pd.to_datetime(daily_df_temp['date']).dt.normalize()
                
                # Finde Index des heutigen Tages
                today = pd.Timestamp.now().normalize()
                today_idx = 0
                for idx, row in daily_df_temp.iterrows():
                    if row['date'] == today:
                        today_idx = idx
                        break
                
                # 7 Tage zurück bis 14 Tage nach vorne
                start_idx = max(0, today_idx - 7)
                end_idx = min(len(daily_df_temp), today_idx + 15)
                
                forecast_display = daily_df_temp.iloc[start_idx:end_idx].copy()
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
                
                st.markdown("---")
                
                # 14-Tage Grafiken
                st.write("**📈 Entwicklung über 14 Tage:**")
                
                # Vorbereitung der Prognosedaten für Charts
                forecast_display['date_str'] = forecast_display['date'].apply(lambda d: format_date_german(d, 'short').split('\n')[0])
                
                # Tabs für Diagramme
                tab_14_temp, tab_14_precip, tab_14_wind, tab_14_cloud, tab_14_snow = st.tabs([
                    "🌡️ Temperatur",
                    "💧 Niederschlag",
                    "💨 Wind",
                    "☁️ Bewölkung",
                    "❄️ Schnee"
                ])
                
                import altair as alt
                
                with tab_14_temp:
                    st.subheader("🌡️ Temperaturverlauf über 14 Tage")
                    temp_cols = ['date_str', 'temperature_2m_max', 'temperature_2m_min', 'apparent_temperature_max', 'apparent_temperature_min']
                    if all(col in forecast_display.columns for col in temp_cols):
                        temp_14 = forecast_display[temp_cols].copy()
                        temp_14.columns = ['Tag', 'Max Temp', 'Min Temp', 'Gefühlte Max', 'Gefühlte Min']
                        
                        # Umwandle in long format für Legende
                        temp_14_long = temp_14.melt(id_vars=['Tag'], var_name='Metrik', value_name='Temperatur')
                        
                        color_scale = alt.Scale(domain=['Max Temp', 'Min Temp', 'Gefühlte Max', 'Gefühlte Min'],
                                                range=['#dc2626', '#3b82f6', '#f97316', '#06b6d4'])
                        stroke_dash_scale = alt.Scale(domain=['Max Temp', 'Min Temp', 'Gefühlte Max', 'Gefühlte Min'],
                                                      range=[[], [], [5, 5], [5, 5]])
                        
                        chart = alt.Chart(temp_14_long).mark_line(point=True, size=2).encode(
                            x=alt.X('Tag', sort=None),
                            y=alt.Y('Temperatur', scale=alt.Scale(zero=False), title='Temperatur (°C)'),
                            color=alt.Color('Metrik', scale=color_scale, legend=alt.Legend(title='Legende')),
                            strokeDash=alt.StrokeDash('Metrik', scale=stroke_dash_scale, legend=None)
                        ).properties(height=400).interactive()
                        st.altair_chart(chart, use_container_width=True)
                        st.dataframe(temp_14, use_container_width=True, hide_index=True)
                    else:
                        st.info("⚠️ Temperaturdaten nicht verfügbar")
                
                with tab_14_precip:
                    st.subheader("💧 Niederschlag über 14 Tage")
                    if 'precipitation_sum' in forecast_display.columns:
                        precip_14 = forecast_display[['date_str', 'precipitation_sum']].copy()
                        precip_14.columns = ['Tag', 'Niederschlag (mm)']
                        
                        chart = alt.Chart(precip_14).mark_bar(color='#06b6d4').encode(
                            x=alt.X('Tag', sort=None),
                            y=alt.Y('Niederschlag (mm)')
                        ).properties(height=400).interactive()
                        
                        st.altair_chart(chart, use_container_width=True)
                        st.dataframe(precip_14, use_container_width=True, hide_index=True)
                    else:
                        st.info("⚠️ Niederschlagsdaten nicht verfügbar")
                
                with tab_14_wind:
                    st.subheader("💨 Windgeschwindigkeit über 14 Tage")
                    # Prüfe ob wind-Spalten existieren
                    if 'wind_speed_10m_max' in forecast_display.columns and 'wind_gusts_10m_max' in forecast_display.columns:
                        wind_14 = forecast_display[['date_str', 'wind_speed_10m_max', 'wind_gusts_10m_max']].copy()
                        wind_14.columns = ['Tag', 'Max Windspeed (km/h)', 'Max Windböen (km/h)']
                        
                        # Umwandle in long format für Legende
                        wind_14_long = wind_14.melt(id_vars=['Tag'], var_name='Metrik', value_name='Windgeschwindigkeit')
                        
                        color_scale = alt.Scale(domain=['Max Windspeed (km/h)', 'Max Windböen (km/h)'],
                                                range=['#10b981', '#ef4444'])
                        stroke_dash_scale = alt.Scale(domain=['Max Windspeed (km/h)', 'Max Windböen (km/h)'],
                                                      range=[[], [5, 5]])
                        
                        chart = alt.Chart(wind_14_long).mark_line(point=True, size=2).encode(
                            x=alt.X('Tag', sort=None),
                            y=alt.Y('Windgeschwindigkeit', scale=alt.Scale(zero=False), title='Windgeschwindigkeit (km/h)'),
                            color=alt.Color('Metrik', scale=color_scale, legend=alt.Legend(title='Legende')),
                            strokeDash=alt.StrokeDash('Metrik', scale=stroke_dash_scale, legend=None)
                        ).properties(height=400).interactive()
                        st.altair_chart(chart, use_container_width=True)
                        st.dataframe(wind_14, use_container_width=True, hide_index=True)
                    else:
                        st.info("⚠️ Windgeschwindigkeitsdaten nicht verfügbar")
                
                with tab_14_cloud:
                    st.subheader("☁️ Wolkenbedeckung über 14 Tage")
                    cloud_14 = forecast_display[['date_str', 'cloud_cover']].copy() if 'cloud_cover' in forecast_display.columns else pd.DataFrame()
                    
                    if not cloud_14.empty:
                        cloud_14.columns = ['Tag', 'Wolkenbedeckung (%)']
                        
                        chart = alt.Chart(cloud_14).mark_bar(color='#94a3b8').encode(
                            x=alt.X('Tag', sort=None),
                            y=alt.Y('Wolkenbedeckung (%)', scale=alt.Scale(domain=[0, 100]))
                        ).properties(height=400)
                        
                        st.altair_chart(chart, use_container_width=True)
                        st.dataframe(cloud_14, use_container_width=True, hide_index=True)
                    else:
                        st.info("Keine Wolkendaten verfügbar")
                
                with tab_14_snow:
                    st.subheader("❄️ Schneefall über 14 Tage")
                    snow_14 = forecast_display[['date_str', 'snowfall_sum']].copy() if 'snowfall_sum' in forecast_display.columns else pd.DataFrame()
                    
                    if not snow_14.empty:
                        snow_14.columns = ['Tag', 'Schneefall (cm)']
                        
                        chart = alt.Chart(snow_14).mark_bar(color='#7dd3fc').encode(
                            x=alt.X('Tag', sort=None),
                            y=alt.Y('Schneefall (cm)')
                        ).properties(height=400)
                        
                        st.altair_chart(chart, use_container_width=True)
                        st.dataframe(snow_14, use_container_width=True, hide_index=True)
                    else:
                        st.info("Keine Schneefalldaten verfügbar")
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
