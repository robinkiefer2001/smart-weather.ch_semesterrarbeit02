import openmeteo_requests
import pandas as pd
import requests
from typing import Dict, Tuple

# User-Agent für API-Requests
USER_AGENT = "smart-ch.ch/1.0 (kontakt@deine-domain.ch)"


def fetch_weather_data(latitude: float, longitude: float) -> Tuple[Dict, pd.DataFrame, pd.DataFrame]:
    """
    Holt Wetterdaten von der Open-Meteo API.
    
    Args:
        latitude: Breitengrad
        longitude: Längengrad
        
    Returns:
        Tuple mit (current_data, hourly_df, daily_df)
    """
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
        "wind_speed_10m": hourly.Variables(21).ValuesAsNumpy(),
        "wind_gusts_10m": hourly.Variables(29).ValuesAsNumpy(),
    })

    # ===== DAILY DATA =====
    daily = response.Daily()
    daily_time = pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s"),
        end=pd.to_datetime(daily.TimeEnd(), unit="s"),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left",
    )

    daily_df = pd.DataFrame({
        "date": daily_time,
        "weather_code": daily.Variables(0).ValuesAsNumpy(),
        "temperature_2m_max": daily.Variables(1).ValuesAsNumpy(),
        "temperature_2m_min": daily.Variables(2).ValuesAsNumpy(),
        "apparent_temperature_max": daily.Variables(3).ValuesAsNumpy(),
        "apparent_temperature_min": daily.Variables(4).ValuesAsNumpy(),
        "sunrise": daily.Variables(5).ValuesAsNumpy(),
        "sunset": daily.Variables(6).ValuesAsNumpy(),
        "daylight_duration": daily.Variables(7).ValuesAsNumpy(),
        "sunshine_duration": daily.Variables(8).ValuesAsNumpy(),
        "uv_index_max": daily.Variables(9).ValuesAsNumpy(),
        "uv_index_clear_sky_max": daily.Variables(10).ValuesAsNumpy(),
        "rain_sum": daily.Variables(11).ValuesAsNumpy(),
        "showers_sum": daily.Variables(12).ValuesAsNumpy(),
        "snowfall_sum": daily.Variables(13).ValuesAsNumpy(),
        "precipitation_sum": daily.Variables(14).ValuesAsNumpy(),
        "precipitation_hours": daily.Variables(15).ValuesAsNumpy(),
        "precipitation_probability_max": daily.Variables(16).ValuesAsNumpy(),
        "wind_speed_10m_max": daily.Variables(17).ValuesAsNumpy() if daily.VariablesLength() > 17 else None,
        "wind_gusts_10m_max": daily.Variables(18).ValuesAsNumpy() if daily.VariablesLength() > 18 else None,
        "shortwave_radiation_sum": daily.Variables(19).ValuesAsNumpy() if daily.VariablesLength() > 19 else None,
        "wind_direction_10m_dominant": daily.Variables(20).ValuesAsNumpy() if daily.VariablesLength() > 20 else None,
    })
    
    # Entferne None-Spalten
    daily_df = daily_df.dropna(axis=1, how='all')
    daily_df = daily_df.drop(columns=[col for col in daily_df.columns if daily_df[col].isnull().all()], errors='ignore')
    
    # Runde numerische Spalten konsistent
    daily_df["temperature_2m_max"] = daily_df["temperature_2m_max"].astype(float).round(2)
    daily_df["temperature_2m_min"] = daily_df["temperature_2m_min"].astype(float).round(2)
    daily_df["apparent_temperature_max"] = daily_df["apparent_temperature_max"].astype(float).round(2)
    daily_df["apparent_temperature_min"] = daily_df["apparent_temperature_min"].astype(float).round(2)
    daily_df["sunshine_duration"] = daily_df["sunshine_duration"].astype(float).round(2)
    daily_df["rain_sum"] = daily_df["rain_sum"].astype(float).round(2)
    daily_df["showers_sum"] = daily_df["showers_sum"].astype(float).round(2)
    daily_df["snowfall_sum"] = daily_df["snowfall_sum"].astype(float).round(2)
    daily_df["precipitation_sum"] = daily_df["precipitation_sum"].astype(float).round(2)
    daily_df["precipitation_hours"] = daily_df["precipitation_hours"].astype(float).round(2)
    daily_df["precipitation_probability_max"] = daily_df["precipitation_probability_max"].astype(float).round(2)
    daily_df["wind_speed_10m_max"] = daily_df["wind_speed_10m_max"].astype(float).round(2)
    daily_df["wind_gusts_10m_max"] = daily_df["wind_gusts_10m_max"].astype(float).round(2)
    daily_df["uv_index_max"] = daily_df["uv_index_max"].astype(float).round(2)
    daily_df["uv_index_clear_sky_max"] = daily_df["uv_index_clear_sky_max"].astype(float).round(2)
    
    # Berechne durchschnittliche cloud_cover pro Tag aus hourly_df
    hourly_df["date"] = hourly_df["time"].dt.date
    daily_cloud_cover = hourly_df.groupby("date")["cloud_cover"].mean().round(2)
    daily_df["cloud_cover"] = daily_df["date"].dt.date.map(daily_cloud_cover).fillna(0)

    return current_data, hourly_df, daily_df


def geocode_multiple(location: str, max_results: int = 5) -> list:
    """
    Holt mehrere geografische Ortsvorschläge für einen gegebenen Ort.
    
    Args:
        location: Name des Ortes (Suchtext)
        max_results: Maximale Anzahl der Ergebnisse (Standard: 5)
        
    Returns:
        Liste von Dictionaries mit Ortsinformationen (name, country, admin1, postcode, latitude, longitude)
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location,
        "format": "json",
        "limit": max_results,
        "addressdetails": 1,
    }
    
    headers = {
        "User-Agent": USER_AGENT
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        responses = response.json()
        results = []
        
        for result in responses:
            result_dict = {
                "name": result.get("name", ""),
                "latitude": float(result.get("lat", 0)),
                "longitude": float(result.get("lon", 0)),
                "country": result.get("address", {}).get("country", ""),
                "postcode": result.get("address", {}).get("postcode", ""),
                "admin1": result.get("address", {}).get("state", ""),  # Kanton/Region/Provinz
            }
            results.append(result_dict)
        
        return results
    except Exception as e:
        print(f"Fehler bei Geocoding: {e}")
        return []