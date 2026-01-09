"""
Wiederverwendbare UI-Komponenten für die Streamlit-App
"""
import streamlit as st
import pandas as pd
from data_handlers import weather_icon, weather_description


def display_current_metrics(current_data: dict):
    """
    Zeigt aktuelle Wetter-Metriken in Spalten an.
    
    Args:
        current_data: Dictionary mit aktuellen Wetterdaten
    """
    metric_col_temp, metric_col_humidity, metric_col_wind = st.columns(3, gap="small")

    with metric_col_temp:
        st.metric("🌡️ Lufttemperatur", 
                 f"{current_data['temperature_2m']:.2f} °C")
        st.metric("🥵 Gefühlte Temp.", 
                 f"{current_data['apparent_temperature']:.2f} °C")

    with metric_col_humidity:
        st.metric("💧 rel. Feuchte", 
                 f"{current_data['relative_humidity_2m']:.0f} %")
        st.metric("☁️ Bewölkung", 
                 f"{current_data['cloud_cover']:.0f} %")

    with metric_col_wind:
        st.metric("🌬️ Wind 10 m", 
                 f"{current_data['wind_speed_10m']:.2f} km/h")
        st.metric("💨 Böen 10 m", 
                 f"{current_data['wind_gusts_10m']:.2f} km/h")


def display_hourly_overview(hourly_df: pd.DataFrame):
    """
    Zeigt stündliche Übersicht in einer Tabelle an.
    
    Args:
        hourly_df: DataFrame mit vorbereiteten stündlichen Daten (muss bereits gefiltert und formatiert sein)
    """
    st.subheader("Stündliche Übersicht für heute:")
    
    # Zeige ausgewählte Spalten mit konfigurierten Spaltenüberschriften
    st.dataframe(
        hourly_df[["time_formatted", "short", "cloud_cover", "temperature_2m", "precipitation", "wind_speed_10m"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "time_formatted": st.column_config.TextColumn("🕐 Uhrzeit", width="small"),
            "short": st.column_config.TextColumn("☁️ Wetter", width="small"),
            "cloud_cover": st.column_config.NumberColumn("☁️ Bewölkung (%)", width="small"),
            "temperature_2m": st.column_config.NumberColumn("🌡️ Temp. (°C)", width="small", format="%.2f"),
            "precipitation": st.column_config.NumberColumn("🌧️ Niederschlag (mm)", width="small", format="%.2f"),
            "wind_speed_10m": st.column_config.NumberColumn("🌬️ Wind (km/h)", width="small", format="%.2f"),
        }
    )


def display_detailed_table(table_df: pd.DataFrame):
    """
    Zeigt detaillierte Tabelle mit allen Wetterdaten an.
    
    Args:
        table_df: Vorbereitetes DataFrame für Tabellenanzeige
    """
    st.subheader("📊 Stündliche Tagesübersicht")
    
    st.dataframe(
        table_df,
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


def display_temperature_chart(chart_df: pd.DataFrame, stats: dict):
    """
    Zeigt Temperatur-Chart mit Statistiken an.
    
    Args:
        chart_df: DataFrame mit Temperaturdaten für Chart
        stats: Dictionary mit Temperaturstatistiken
    """
    st.line_chart(
        data=chart_df.set_index("Uhrzeit")[
            ["Absolute Temperatur (°C)", "Temperaturveränderung (°C)"]
        ],
        height=400,
        use_container_width=True
    )

    temp_metric_col1, temp_metric_col2, temp_metric_col3, temp_metric_col4 = st.columns(4)
    with temp_metric_col1:
        st.metric("🌡️ Max. Temperatur", f"{stats['max_temp']:.2f} °C")
    with temp_metric_col2:
        st.metric("🥶 Min. Temperatur", f"{stats['min_temp']:.2f} °C")
    with temp_metric_col3:
        st.metric("📈 Grösster Anstieg", f"+{stats['max_increase']:.2f} °C/h")
    with temp_metric_col4:
        st.metric("📉 Grösster Rückgang", f"{stats['max_decrease']:.2f} °C/h")


def display_precipitation_chart(chart_df: pd.DataFrame, stats: dict):
    """
    Zeigt Niederschlags-Chart mit Statistiken an.
    
    Args:
        chart_df: DataFrame mit Niederschlagsdaten für Chart
        stats: Dictionary mit Niederschlagsstatistiken
    """
    st.line_chart(
        data=chart_df.set_index("Uhrzeit")[
            ["Regen (mm)", "Schauer (mm)"]
        ],
        height=400,
        use_container_width=True
    )

    precip_metric_col1, precip_metric_col2, precip_metric_col3 = st.columns(3)
    with precip_metric_col1:
        st.metric("🌧️ Regen (gesamt)", f"{stats['total_rain']:.2f} mm")
    with precip_metric_col2:
        st.metric("⛈️ Schauer (gesamt)", f"{stats['total_showers']:.2f} mm")
    with precip_metric_col3:
        st.metric("💧 Gesamtniederschlag", f"{stats['total_precipitation']:.2f} mm")


def display_wind_chart(chart_df: pd.DataFrame, stats: dict):
    """
    Zeigt Wind-Chart mit Statistiken an.
    
    Args:
        chart_df: DataFrame mit Winddaten für Chart
        stats: Dictionary mit Windstatistiken
    """
    st.line_chart(
        data=chart_df.set_index("Uhrzeit")[
            ["Wind (km/h)", "Böen (km/h)"]
        ],
        height=400,
        use_container_width=True
    )

    wind_metric_col1, wind_metric_col2 = st.columns(2)
    with wind_metric_col1:
        st.metric("🌬️ Max. Wind", f"{stats['max_wind']:.2f} km/h")
    with wind_metric_col2:
        st.metric("💨 Max. Böen", f"{stats['max_gusts']:.2f} km/h")


def display_cloud_chart(chart_df: pd.DataFrame, stats: dict):
    """
    Zeigt Bewölkungs-Chart mit Statistiken an.
    
    Args:
        chart_df: DataFrame mit Bewölkungsdaten für Chart
        stats: Dictionary mit Bewölkungsstatistiken
    """
    st.line_chart(
        data=chart_df.set_index("Uhrzeit")[
            ["Bewölkung (%)"]
        ],
        height=400,
        use_container_width=True
    )

    st.metric("☁️ Durchschnittl. Bewölkung", f"{stats['avg_cloud_cover']:.0f} %")


def display_snow_chart(chart_df: pd.DataFrame, stats: dict):
    """
    Zeigt Schneefalls-Chart mit Statistiken an.
    
    Args:
        chart_df: DataFrame mit Schneefallsdaten für Chart
        stats: Dictionary mit Schneefallsstatistiken
    """
    st.line_chart(
        data=chart_df.set_index("Uhrzeit")[
            ["Schneefall (cm)"]
        ],
        height=400,
        use_container_width=True
    )

    st.metric("❄️ Gesamtschneefall", f"{stats['total_snowfall']:.2f} cm")

# ===== LOCATION & SEARCH UI =====
def display_location_search_section():
    """
    Zeigt Suchbereich mit Textfeld, Button und Vorschlagsliste an.
    Verwaltet location_search_pending, location_chosen, location_suggestions in session_state.
    """
    # Pending-Wert verarbeiten (von Button-Klick aus)
    if st.session_state.location_search_pending is not None:
        pending_value = st.session_state.location_search_pending
        st.session_state.location_search = pending_value
        st.session_state.location_search_pending = None
        st.rerun()

    col_search, col_button = st.columns([3, 1])

    with col_search:
        search_query = st.text_input(
            label="",
            placeholder="🔍 Ort suchen (z.B. 'Bern', 'Zürich', 'Genf')",
            key="location_search",
        )

    with col_button:
        st.write("")  # Spacer für Alignment
        search_button = st.button("Suchen", use_container_width=True)

    return search_query, search_button


def display_location_suggestions(suggestions):
    """
    Zeigt Button-basierte Trefferliste und Auto-Auswahl-Logik.
    
    Args:
        suggestions: Liste von (label, result) Tupeln
    
    Returns:
        Tuple: (label, result) der ausgewählten Location oder (None, None)
    """
    selected_label = None
    selected_result = None
    
    if len(suggestions) > 1 and not st.session_state.location_chosen:
        st.write("**Verfügbare Orte:**")
        for label, result in suggestions:
            if st.button(label, use_container_width=True, key=f"sugg_{label}"):
                selected_label = label
                selected_result = result
                return selected_label, selected_result
    elif len(suggestions) == 1 and not st.session_state.location_chosen:
        st.caption("✓ 1 Treffer gefunden – wird automatisch verwendet.")
        label, result = suggestions[0]
        return label, result
    
    return None, None


def display_map_legend():
    """Zeigt interaktive Kartenlegende an."""
    with st.expander("Kartenlegende", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Temperaturbereich:**
            - Unter -5°C (sehr kalt)
            - -5 bis 0°C (kalt)
            - 0 bis 10°C (kühl)
            - 10 bis 15°C (temperiert)
            - 15 bis 20°C (mild)
            - Über 20°C (warm)
            """)
        with col2:
            st.markdown("""
            **Wetterzustände:**
            - Sonnig / Heiter
            - Teilweise bewölkt
            - Bewölkt
            - Regnerisch
            - Schneefall
            - Gewitter
            """)


def display_day_card(date_obj, row, today, format_date_german_func, weather_icon_func):
    """
    Zeigt eine einzelne Tages-Karte an.
    
    Args:
        date_obj: datetime.date Objekt
        row: pandas Series mit Wetterdaten
        today: datetime.date für Heute-Markierung
        format_date_german_func: Funktion zum Formatieren von Daten auf Deutsch
        weather_icon_func: Funktion zur Rückgabe von Wetter-Emoji
    
    Returns:
        HTML-String für die Karte
    """
    date_str = format_date_german_func(date_obj, 'short')
    temp_max = row.get('temperature_2m_max', '--')
    temp_min = row.get('temperature_2m_min', '--')
    precip = row.get('precipitation_sum', 0)
    weather_code = int(row.get('weather_code', 0))
    emoji = weather_icon_func(weather_code) or "🌤️"

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

    # Markiere heutigen Tag
    is_today = date_obj == today
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

    return f"""
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
    """


def display_location_selected_message(display_name):
    """Zeigt Erfolgs-Meldung nach Ort-Auswahl."""
    st.success(f"✅ Ort ausgewählt: **{display_name}**")