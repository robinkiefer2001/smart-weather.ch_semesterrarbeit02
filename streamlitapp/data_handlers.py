"""
Datenverarbeitung und Business-Logik für Wetterdaten
"""
import pandas as pd
import datetime


def weather_icon(weather_code: int) -> str:
    """
    Konvertiert einen Weather Code in ein Emoji-Icon.
    WMO Weather Interpretation Codes (www.wmo.int/www/WMOguide/Guide-wtc78Eng-2012.pdf)
    
    Args:
        weather_code: WMO Weather Code (0-99)
        
    Returns:
        Emoji-Icon als String
    """
    weather_icons = {
        # Klare/Bewölkte Codes (0-19)
        0: "☀️",      # Klar / Wolkenlos
        1: "🌤️",     # Überwiegend klar
        2: "⛅",      # Teilweise bewölkt / Variable Bewölkung
        3: "☁️",      # Bedeckt
        4: "💨",      # Sicht durch Rauch vermindert
        5: "🌫️",     # Trockener Dunst
        6: "🏭",      # Verbreiteter Schwebstaub
        7: "🌪️",     # Staub vom Wind
        8: "🌪️",     # Staub- oder Sandwirbel
        9: "🌪️",     # Staub- oder Sandsturm
        10: "🌫️",    # Feuchter Dunst
        11: "🌫️",    # Bodennebel (Schwaden)
        12: "🌫️",    # Durchgehender Bodennebel
        13: "⚡",     # Wetterleuchten
        14: "💧",     # Niederschlag (Boden nicht erreichbar)
        15: "🌧️",    # Niederschlag in Ferne
        16: "🌧️",    # Niederschlag in Nähe
        17: "⛈️",    # Gewitter ohne Niederschlag
        18: "💨",     # Markante Böen
        19: "🌪️",    # Tromben/Windhose
        
        # Ereignisse der letzten Stunde (20-29)
        20: "💧",     # Nach Sprühregen
        21: "🌦️",    # Nach Regen
        22: "❄️",     # Nach Schneefall
        23: "🌧️",    # Nach Schneeregen
        24: "🌧️",    # Nach gefrierendem Regen
        25: "🌧️",    # Nach Regenschauer
        26: "❄️",     # Nach Schneeschauer
        27: "🌧️",    # Nach Graupel-/Hagelschauer
        28: "🌫️",    # Nach Nebel
        29: "⛈️",    # Nach Gewitter
        
        # Sandsturm, Schneefegen (30-39)
        30: "🌪️",    # Sandsturm (abnehmend)
        31: "🌪️",    # Sandsturm (gleichbleibend)
        32: "🌪️",    # Sandsturm (zunehmend)
        33: "🌪️",    # Schwerer Sandsturm (abnehmend)
        34: "🌪️",    # Schwerer Sandsturm (gleichbleibend)
        35: "🌪️",    # Schwerer Sandsturm (zunehmend)
        36: "❄️",     # Leichtes Schneefegen
        37: "❄️",     # Starkes Schneefegen
        38: "❄️",     # Leichtes Schneetreiben
        39: "❄️",     # Starkes Schneetreiben
        
        # Nebel oder Eisnebel (40-49)
        40: "🌫️",    # Nebel in Ferne
        41: "🌫️",    # Nebel in Schwaden
        42: "🌫️",    # Nebel (dünner werdend, Himmel sichtbar)
        43: "🌫️",    # Nebel (dünner werdend, Himmel verdeckt)
        44: "🌫️",    # Nebel (gleichbleibend, Himmel sichtbar)
        45: "🌫️",    # Nebel (gleichbleibend, Himmel verdeckt)
        46: "🌫️",    # Nebel (dichter werdend, Himmel sichtbar)
        47: "🌫️",    # Nebel (dichter werdend, Himmel verdeckt)
        48: "🌫️",    # Nebel mit Reif
        49: "🌫️",    # Nebel mit Reif (Himmel verdeckt)
        
        # Sprühregen (50-59)
        50: "🌦️",    # Leichter Sprühregen (unterbrochen)
        51: "🌦️",    # Leichter Sprühregen
        52: "🌦️",    # Mässiger Sprühregen (unterbrochen)
        53: "🌦️",    # Mässiger Sprühregen
        54: "🌦️",    # Starker Sprühregen (unterbrochen)
        55: "🌦️",    # Starker Sprühregen
        56: "🌧️",    # Leichter gefrierender Sprühregen
        57: "🌧️",    # Starker gefrierender Sprühregen
        58: "🌧️",    # Leichter Sprühregen mit Regen
        59: "🌧️",    # Starker Sprühregen mit Regen
        
        # Regen (60-69)
        60: "🌦️",    # Leichter Regen (unterbrochen)
        61: "🌧️",    # Leichter Regen
        62: "🌧️",    # Mässiger Regen (unterbrochen)
        63: "🌧️",    # Mässiger Regen
        64: "🌧️",    # Starker Regen (unterbrochen)
        65: "🌧️",    # Starker Regen
        66: "🌧️",    # Leichter gefrierender Regen
        67: "🌧️",    # Starker gefrierender Regen
        68: "🌧️",    # Leichter Schneeregen
        69: "🌧️",    # Starker Schneeregen
        
        # Schnee (70-79)
        70: "❄️",     # Leichter Schneefall (unterbrochen)
        71: "❄️",     # Leichter Schneefall
        72: "❄️",     # Mässiger Schneefall (unterbrochen)
        73: "❄️",     # Mässiger Schneefall
        74: "❄️",     # Starker Schneefall (unterbrochen)
        75: "❄️",     # Starker Schneefall
        76: "❄️",     # Eisnadeln
        77: "❄️",     # Schneegriesel
        78: "❄️",     # Schneekristalle
        79: "❄️",     # Eiskörner
        
        # Schauer (80-90)
        80: "🌧️",    # Leichter Regenschauer
        81: "🌧️",    # Regenschauer
        82: "🌧️",    # Starker Regenschauer
        83: "🌧️",    # Leichter Schneeregenschauer
        84: "🌧️",    # Starker Schneeregenschauer
        85: "❄️",     # Leichter Schneeschauer
        86: "❄️",     # Schneeschauer
        87: "🌧️",    # Leichter Graupelschauer
        88: "🌧️",    # Graupelschauer
        89: "🌧️",    # Leichter Hagelschauer
        90: "🌧️",    # Hagelschauer
        
        # Gewitter (91-99)
        91: "⛈️",    # Gewitter mit leichtem Regen
        92: "⛈️",    # Gewitter mit starkem Regen
        93: "⛈️",    # Gewitter mit leichtem Schneefall
        94: "⛈️",    # Gewitter mit starkem Schneefall
        95: "⛈️",    # Gewitter mit Regen
        96: "⛈️",    # Gewitter mit Graupel/Hagel
        97: "⛈️",    # Starkes Gewitter
        98: "⛈️",    # Gewitter mit Sandsturm
        99: "⛈️",    # Starkes Gewitter mit Hagel
    }
    return weather_icons.get(weather_code, "🌤️")  # Fallback zu schönem Wetter


def weather_description(weather_code: int) -> str:
    """
    Konvertiert einen Weather Code in eine Textbeschreibung.
    
    Args:
        weather_code: WMO Weather Code
        
    Returns:
        Beschreibung als String
    """
    weather_descriptions = {
        # Bewölkungsentwicklung
        0: "Klar / Wolkenlos",
        1: "Überwiegend klar",
        2: "Teilweise bewölkt",
        3: "Bedeckt",
        
        # Dunst, Rauch, Staub oder Sand
        4: "Sicht durch Rauch/Asche vermindert",
        5: "Trockener Dunst",
        6: "Verbreiteter Schwebstaub",
        7: "Staub oder Sand (vom Wind)",
        8: "Staub- oder Sandwirbel",
        9: "Staub- oder Sandsturm in Sicht",
        
        # Trockenereignisse
        10: "Feuchter Dunst",
        11: "Bodennebel (Schwaden)",
        12: "Durchgehender Bodennebel",
        13: "Wetterleuchten",
        14: "Niederschlag (Boden nicht erreichend)",
        15: "Niederschlag in der Ferne",
        16: "Niederschlag in der Nähe",
        17: "Gewitter ohne Niederschlag",
        18: "Markante Böen",
        19: "Tromben/Windhose",
        
        # Ereignisse der letzten Stunde
        20: "Nach Sprühregen",
        21: "Nach Regen",
        22: "Nach Schneefall",
        23: "Nach Schneeregen",
        24: "Nach gefrierendem Regen",
        25: "Nach Regenschauer",
        26: "Nach Schneeschauer",
        27: "Nach Graupel-/Hagelschauer",
        28: "Nach Nebel",
        29: "Nach Gewitter",
        
        # Staubsturm, Sandsturm, Schneefegen
        30: "Sandsturm (abnehmend)",
        31: "Sandsturm (gleichbleibend)",
        32: "Sandsturm (zunehmend)",
        33: "Schwerer Sandsturm (abnehmend)",
        34: "Schwerer Sandsturm (gleichbleibend)",
        35: "Schwerer Sandsturm (zunehmend)",
        36: "Leichtes Schneefegen",
        37: "Starkes Schneefegen",
        38: "Leichtes Schneetreiben",
        39: "Starkes Schneetreiben",
        
        # Nebel oder Eisnebel
        40: "Nebel in der Ferne",
        41: "Nebel in Schwaden",
        42: "Nebel (dünner werdend, Himmel sichtbar)",
        43: "Nebel (dünner werdend, Himmel verdeckt)",
        44: "Nebel (gleichbleibend, Himmel sichtbar)",
        45: "Nebel (gleichbleibend, Himmel verdeckt)",
        46: "Nebel (dichter werdend, Himmel sichtbar)",
        47: "Nebel (dichter werdend, Himmel verdeckt)",
        48: "Nebel mit Reif (Himmel sichtbar)",
        49: "Nebel mit Reif (Himmel verdeckt)",
        
        # Sprühregen
        50: "Leichter Sprühregen (unterbrochen)",
        51: "Leichter Sprühregen",
        52: "Mässiger Sprühregen (unterbrochen)",
        53: "Mässiger Sprühregen",
        54: "Starker Sprühregen (unterbrochen)",
        55: "Starker Sprühregen",
        56: "Leichter gefrierender Sprühregen",
        57: "Starker gefrierender Sprühregen",
        58: "Leichter Sprühregen mit Regen",
        59: "Starker Sprühregen mit Regen",
        
        # Regen
        60: "Leichter Regen (unterbrochen)",
        61: "Leichter Regen",
        62: "Mässiger Regen (unterbrochen)",
        63: "Mässiger Regen",
        64: "Starker Regen (unterbrochen)",
        65: "Starker Regen",
        66: "Leichter gefrierender Regen",
        67: "Starker gefrierender Regen",
        68: "Leichter Schneeregen",
        69: "Starker Schneeregen",
        
        # Schnee
        70: "Leichter Schneefall (unterbrochen)",
        71: "Leichter Schneefall",
        72: "Mässiger Schneefall (unterbrochen)",
        73: "Mässiger Schneefall",
        74: "Starker Schneefall (unterbrochen)",
        75: "Starker Schneefall",
        76: "Eisnadeln",
        77: "Schneegriesel",
        78: "Schneekristalle",
        79: "Eiskörner",
        
        # Schauer
        80: "Leichter Regenschauer",
        81: "Regenschauer",
        82: "Starker Regenschauer",
        83: "Leichter Schneeregenschauer",
        84: "Starker Schneeregenschauer",
        85: "Leichter Schneeschauer",
        86: "Schneeschauer",
        87: "Leichter Graupelschauer",
        88: "Graupelschauer",
        89: "Leichter Hagelschauer",
        90: "Hagelschauer",
        
        # Gewitter
        91: "Gewitter mit leichtem Regen",
        92: "Gewitter mit starkem Regen",
        93: "Gewitter mit leichtem Schneefall",
        94: "Gewitter mit starkem Schneefall",
        95: "Gewitter mit Regen",
        96: "Gewitter mit Graupel/Hagel",
        97: "Starkes Gewitter",
        98: "Gewitter mit Sandsturm",
        99: "Starkes Gewitter mit Hagel"
    }
    return weather_descriptions.get(weather_code, "")


def filter_today_data(hourly_df: pd.DataFrame, target_date: datetime.date = None) -> pd.DataFrame:
    """
    Filtert stündliche Daten für einen bestimmten Tag.
    
    Args:
        hourly_df: DataFrame mit stündlichen Wetterdaten
        target_date: Zieldatum (Standard: heute)
        
    Returns:
        Gefiltertes und sortiertes DataFrame
    """
    if target_date is None:
        target_date = datetime.date.today()
    
    return hourly_df[hourly_df['time'].dt.date == target_date].copy().sort_values("time")


def prepare_hourly_overview(hourly_df: pd.DataFrame, target_date: datetime.date = None) -> pd.DataFrame:
    """
    Bereitet stündliche Übersicht mit Icons und Beschreibungen vor.
    
    Args:
        hourly_df: DataFrame mit stündlichen Wetterdaten
        target_date: Zieldatum (Standard: heute)
        
    Returns:
        DataFrame mit zusätzlichen Spalten für Anzeige
    """
    # Filtere Daten für das Zieldatum
    df = filter_today_data(hourly_df, target_date).copy()
    
    # Formatiere Uhrzeit als HH:MM String (für Übersicht) - speichere in neuer Spalte
    df["time_formatted"] = df["time"].dt.strftime("%H:%M")
    
    # Erstelle Wetter-Icons und Beschreibungen
    df["icon"] = df["weather_code"].apply(weather_icon)
    df["description"] = df["weather_code"].apply(weather_description)
    df["short"] = df["icon"] + " " + df["description"]
    
    # Runde numerische Werte konsistent
    df["temperature_2m"] = df["temperature_2m"].round(2)
    df["precipitation"] = df["precipitation"].round(2)
    df["cloud_cover"] = df["cloud_cover"].round(0).astype(int)
    df["wind_speed_10m"] = df["wind_speed_10m"].round(2)
    
    return df


def prepare_table_display(hourly_df: pd.DataFrame, target_date: datetime.date = None) -> pd.DataFrame:
    """
    Bereitet Daten für Tabellenanzeige vor.
    
    Args:
        hourly_df: DataFrame mit stündlichen Wetterdaten
        target_date: Zieldatum (Standard: heute)
        
    Returns:
        Formatiertes DataFrame für Anzeige
    """
    # Filtere Daten für das Zieldatum
    df = filter_today_data(hourly_df, target_date)
    
    # Wähle relevante Spalten aus
    table_df = df[[
        "time", "temperature_2m", "apparent_temperature",
        "relative_humidity_2m", "precipitation",
        "cloud_cover", "wind_speed_10m", "wind_gusts_10m"
    ]].copy()

    # Benenne Spalten mit Emojis um
    table_df.columns = [
        "🕐 Uhrzeit", "🌡️ Temp. (°C)", "🥵 Gefühlt (°C)",
        "💧 Feuchte (%)", "🌧️ Niederschlag (mm)",
        "☁️ Bewölkung (%)", "🌬️ Wind (km/h)", "💨 Böen (km/h)"
    ]
    
    # Formatiere Uhrzeit als HH:MM
    table_df["🕐 Uhrzeit"] = table_df["🕐 Uhrzeit"].dt.strftime("%H:%M")
    
    # Runde Temperaturwerte auf 1 Dezimalstelle
    table_df["🌡️ Temp. (°C)"] = table_df["🌡️ Temp. (°C)"].round(2)
    table_df["🥵 Gefühlt (°C)"] = table_df["🥵 Gefühlt (°C)"].round(2)
    
    # Runde Prozent-Werte auf ganze Zahlen
    table_df["💧 Feuchte (%)"] = table_df["💧 Feuchte (%)"].round(0).astype(int)
    table_df["☁️ Bewölkung (%)"] = table_df["☁️ Bewölkung (%)"].round(0).astype(int)
    
    # Runde Niederschlag und Wind auf 1 Dezimalstelle
    table_df["🌧️ Niederschlag (mm)"] = table_df["🌧️ Niederschlag (mm)"].round(2)
    table_df["🌬️ Wind (km/h)"] = table_df["🌬️ Wind (km/h)"].round(2)
    table_df["💨 Böen (km/h)"] = table_df["💨 Böen (km/h)"].round(2)
    
    return table_df


def prepare_temperature_chart(hourly_df: pd.DataFrame, target_date: datetime.date = None) -> pd.DataFrame:
    """
    Bereitet Temperaturdaten für Chart vor.
    
    Args:
        hourly_df: DataFrame mit stündlichen Wetterdaten
        target_date: Zieldatum (Standard: heute)
        
    Returns:
        DataFrame mit Temperaturverläufen
    """
    # Filtere Daten für das Zieldatum
    df = filter_today_data(hourly_df, target_date)
    
    # Berechne stündliche Temperaturveränderung
    df["temp_change"] = df["temperature_2m"].diff().fillna(0)
    
    # Erstelle Chart-DataFrame mit formatierten Werten
    chart_df = df.copy()
    chart_df["Uhrzeit"] = chart_df["time"].dt.strftime("%H:%M")
    chart_df["Absolute Temperatur (°C)"] = chart_df["temperature_2m"].round(2)
    chart_df["Temperaturveränderung (°C)"] = chart_df["temp_change"].round(2)
    
    return chart_df


def calculate_temperature_stats(hourly_df: pd.DataFrame, target_date: datetime.date = None) -> dict:
    """
    Berechnet Temperaturstatistiken.
    
    Args:
        hourly_df: DataFrame mit stündlichen Wetterdaten
        target_date: Zieldatum (Standard: heute)
        
    Returns:
        Dictionary mit Statistiken (max_temp, min_temp, max_increase, max_decrease)
    """
    # Filtere Daten für das Zieldatum
    df = filter_today_data(hourly_df, target_date)
    
    # Berechne stündliche Temperaturveränderung
    df["temp_change"] = df["temperature_2m"].diff().fillna(0)
    
    return {
        "max_temp": df["temperature_2m"].max(),
        "min_temp": df["temperature_2m"].min(),
        "max_increase": df["temp_change"].max(),
        "max_decrease": df["temp_change"].min()
    }


def prepare_precipitation_chart(hourly_df: pd.DataFrame, target_date: datetime.date = None) -> pd.DataFrame:
    """
    Bereitet Niederschlagsdaten für Chart vor.
    
    Args:
        hourly_df: DataFrame mit stündlichen Wetterdaten
        target_date: Zieldatum (Standard: heute)
        
    Returns:
        DataFrame mit Niederschlagsdaten (Regen und Schauer getrennt)
    """
    # Filtere Daten für das Zieldatum
    df = filter_today_data(hourly_df, target_date)
    
    # Erstelle Chart-DataFrame mit formatierten Werten
    chart_df = df.copy()
    chart_df["Uhrzeit"] = chart_df["time"].dt.strftime("%H:%M")
    chart_df["Regen (mm)"] = chart_df["rain"].round(2)
    chart_df["Schauer (mm)"] = chart_df["showers"].round(2)
    
    return chart_df


def calculate_precipitation_stats(hourly_df: pd.DataFrame, target_date: datetime.date = None) -> dict:
    """
    Berechnet Niederschlagsstatistiken.
    
    Args:
        hourly_df: DataFrame mit stündlichen Wetterdaten
        target_date: Zieldatum (Standard: heute)
        
    Returns:
        Dictionary mit Statistiken (total_rain, total_showers, total_precipitation)
    """
    # Filtere Daten für das Zieldatum
    df = filter_today_data(hourly_df, target_date)
    
    # Berechne Summen für verschiedene Niederschlagsarten
    return {
        "total_rain": df["rain"].sum(),
        "total_showers": df["showers"].sum(),
        "total_precipitation": df["rain"].sum() + df["showers"].sum()
    }


def prepare_wind_chart(hourly_df: pd.DataFrame, target_date: datetime.date = None) -> pd.DataFrame:
    """
    Bereitet Winddaten für Chart vor.
    
    Args:
        hourly_df: DataFrame mit stündlichen Wetterdaten
        target_date: Zieldatum (Standard: heute)
        
    Returns:
        DataFrame mit Winddaten (Windgeschwindigkeit und Böen)
    """
    # Filtere Daten für das Zieldatum
    df = filter_today_data(hourly_df, target_date)
    
    # Erstelle Chart-DataFrame mit formatierten Werten
    chart_df = df.copy()
    chart_df["Uhrzeit"] = chart_df["time"].dt.strftime("%H:%M")
    chart_df["Wind (km/h)"] = chart_df["wind_speed_10m"].round(2)
    chart_df["Böen (km/h)"] = chart_df["wind_gusts_10m"].round(2)
    
    return chart_df


def calculate_wind_stats(hourly_df: pd.DataFrame, target_date: datetime.date = None) -> dict:
    """
    Berechnet Windstatistiken.
    
    Args:
        hourly_df: DataFrame mit stündlichen Wetterdaten
        target_date: Zieldatum (Standard: heute)
        
    Returns:
        Dictionary mit Statistiken (max_wind, max_gusts)
    """
    # Filtere Daten für das Zieldatum
    df = filter_today_data(hourly_df, target_date)
    
    # Berechne maximale Werte
    return {
        "max_wind": df["wind_speed_10m"].max(),
        "max_gusts": df["wind_gusts_10m"].max()
    }


def prepare_cloud_chart(hourly_df: pd.DataFrame, target_date: datetime.date = None) -> pd.DataFrame:
    """
    Bereitet Bewölkungsdaten für Chart vor.
    
    Args:
        hourly_df: DataFrame mit stündlichen Wetterdaten
        target_date: Zieldatum (Standard: heute)
        
    Returns:
        DataFrame mit Bewölkungsdaten in Prozent
    """
    # Filtere Daten für das Zieldatum
    df = filter_today_data(hourly_df, target_date)
    
    # Erstelle Chart-DataFrame mit formatierten Werten
    chart_df = df.copy()
    chart_df["Uhrzeit"] = chart_df["time"].dt.strftime("%H:%M")
    chart_df["Bewölkung (%)"] = chart_df["cloud_cover"].round(0).astype(int)
    
    return chart_df


def calculate_cloud_stats(hourly_df: pd.DataFrame, target_date: datetime.date = None) -> dict:
    """
    Berechnet Bewölkungsstatistiken.
    
    Args:
        hourly_df: DataFrame mit stündlichen Wetterdaten
        target_date: Zieldatum (Standard: heute)
        
    Returns:
        Dictionary mit Statistiken (avg_cloud_cover)
    """
    # Filtere Daten für das Zieldatum
    df = filter_today_data(hourly_df, target_date)
    
    # Berechne Durchschnittswert
    return {
        "avg_cloud_cover": df["cloud_cover"].mean()
    }


def prepare_snow_chart(hourly_df: pd.DataFrame, target_date: datetime.date = None) -> pd.DataFrame:
    """
    Bereitet Schneefallsdaten für Chart vor.
    
    Args:
        hourly_df: DataFrame mit stündlichen Wetterdaten
        target_date: Zieldatum (Standard: heute)
        
    Returns:
        DataFrame mit Schneefallsdaten in Zentimetern
    """
    # Filtere Daten für das Zieldatum
    df = filter_today_data(hourly_df, target_date)
    
    # Erstelle Chart-DataFrame mit formatierten Werten
    chart_df = df.copy()
    chart_df["Uhrzeit"] = chart_df["time"].dt.strftime("%H:%M")
    chart_df["Schneefall (cm)"] = chart_df["snowfall"].round(2)
    
    return chart_df


def calculate_snow_stats(hourly_df: pd.DataFrame, target_date: datetime.date = None) -> dict:
    """
    Berechnet Schneefallstatistiken.
    
    Args:
        hourly_df: DataFrame mit stündlichen Wetterdaten
        target_date: Zieldatum (Standard: heute)
        
    Returns:
        Dictionary mit Statistiken (total_snowfall)
    """
    # Filtere Daten für das Zieldatum
    df = filter_today_data(hourly_df, target_date)
    
    # Berechne Gesamtmenge
    return {
        "total_snowfall": df["snowfall"].sum()
    }
