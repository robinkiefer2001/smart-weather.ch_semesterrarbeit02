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
        hourly_df[["time", "short", "cloud_cover", "temperature_2m", "precipitation", "wind_speed_10m"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "time": st.column_config.TextColumn("🕐 Uhrzeit", width="small"),
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
    st.subheader("📈 Temperaturverlauf")
    
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
    st.subheader("🌧️ Niederschlag")
    
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
    st.subheader("🌬️ Wind")
    
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
    st.subheader("☁️ Bewölkung")
    
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
    st.subheader("❄️ Schneefall")
    
    st.line_chart(
        data=chart_df.set_index("Uhrzeit")[
            ["Schneefall (cm)"]
        ],
        height=400,
        use_container_width=True
    )

    st.metric("❄️ Gesamtschneefall", f"{stats['total_snowfall']:.2f} cm")
