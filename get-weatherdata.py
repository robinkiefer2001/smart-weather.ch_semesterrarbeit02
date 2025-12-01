import psycopg
import pandas as pd
import requests_cache
import openmeteo_requests
from retry_requests import retry
import os
import time
from datetime import datetime, timezone
from insert_weather_data import insert_weather_data
import logging

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Umgebungsvariablen laden
DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = int(os.environ.get("DB_PORT", 5432))

connection_string = (
    f"host={DB_HOST} "
    f"dbname={DB_NAME} "
    f"user={DB_USER} "
    f"password={DB_PASSWORD} "
    f"port={DB_PORT}"
)

# Orte aus Datenbank abrufen
locations = []
logger.info("Lade Orte aus der Datenbank...")

with psycopg.connect(connection_string) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT latitude, longitude FROM geo_location;")
        locations = cur.fetchall()

logger.info(f"Insgesamt {len(locations)} Orte gefunden")

# Pro Ort: Wetterdaten abrufen und speichern
for idx, (latitude, longitude) in enumerate(locations, 1):
    logger.info(f"[{idx}/{len(locations)}] Verarbeite Location: {latitude}, {longitude}")
    
    try:
        # API Setup
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

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

        logger.info(f"Rufe Open-Meteo API auf für ({latitude}, {longitude})...")
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        logger.info(f"Koordinaten: {response.Latitude()}°N {response.Longitude()}°E")
        logger.info(f"Elevation: {response.Elevation()} m asl")

        # ===== CURRENT DATA =====
        logger.info("Verarbeite aktuelle Daten...")
        current = response.Current()
        
        current_dict = {
            'time': current.Time(),
            'temperature_2m': current.Variables(0).Value(),
            'relative_humidity_2m': current.Variables(1).Value(),
            'apparent_temperature': current.Variables(2).Value(),
            'is_day': current.Variables(3).Value(),
            'precipitation': current.Variables(4).Value(),
            'rain': current.Variables(5).Value(),
            'showers': current.Variables(6).Value(),
            'snowfall': current.Variables(7).Value(),
            'weather_code': current.Variables(8).Value(),
            'cloud_cover': current.Variables(9).Value(),
            'pressure_msl': current.Variables(10).Value(),
            'surface_pressure': current.Variables(11).Value(),
            'wind_speed_10m': current.Variables(12).Value(),
            'wind_direction_10m': current.Variables(13).Value(),
            'wind_gusts_10m': current.Variables(14).Value(),
        }

        logger.info(f"Aktuelle Temperatur: {current_dict['temperature_2m']}°C")

        # ===== HOURLY DATA =====
        logger.info("Verarbeite stündliche Daten...")
        hourly = response.Hourly()

        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
        hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
        hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
        hourly_precipitation_probability = hourly.Variables(4).ValuesAsNumpy()
        hourly_precipitation = hourly.Variables(5).ValuesAsNumpy()
        hourly_rain = hourly.Variables(6).ValuesAsNumpy()
        hourly_showers = hourly.Variables(7).ValuesAsNumpy()
        hourly_snow_depth = hourly.Variables(8).ValuesAsNumpy()
        hourly_snowfall = hourly.Variables(9).ValuesAsNumpy()
        hourly_weather_code = hourly.Variables(10).ValuesAsNumpy()
        hourly_surface_pressure = hourly.Variables(11).ValuesAsNumpy()
        hourly_pressure_msl = hourly.Variables(12).ValuesAsNumpy()
        hourly_cloud_cover = hourly.Variables(13).ValuesAsNumpy()
        hourly_cloud_cover_low = hourly.Variables(14).ValuesAsNumpy()
        hourly_cloud_cover_mid = hourly.Variables(15).ValuesAsNumpy()
        hourly_cloud_cover_high = hourly.Variables(16).ValuesAsNumpy()
        hourly_visibility = hourly.Variables(17).ValuesAsNumpy()
        hourly_evapotranspiration = hourly.Variables(18).ValuesAsNumpy()
        hourly_et0_fao_evapotranspiration = hourly.Variables(19).ValuesAsNumpy()
        hourly_vapour_pressure_deficit = hourly.Variables(20).ValuesAsNumpy()
        hourly_wind_speed_10m = hourly.Variables(21).ValuesAsNumpy()
        hourly_wind_speed_80m = hourly.Variables(22).ValuesAsNumpy()
        hourly_wind_speed_120m = hourly.Variables(23).ValuesAsNumpy()
        hourly_wind_speed_180m = hourly.Variables(24).ValuesAsNumpy()
        hourly_wind_direction_10m = hourly.Variables(25).ValuesAsNumpy()
        hourly_wind_direction_80m = hourly.Variables(26).ValuesAsNumpy()
        hourly_wind_direction_180m = hourly.Variables(27).ValuesAsNumpy()
        hourly_wind_direction_120m = hourly.Variables(28).ValuesAsNumpy()
        hourly_wind_gusts_10m = hourly.Variables(29).ValuesAsNumpy()
        hourly_temperature_80m = hourly.Variables(30).ValuesAsNumpy()
        hourly_temperature_120m = hourly.Variables(31).ValuesAsNumpy()
        hourly_temperature_180m = hourly.Variables(32).ValuesAsNumpy()
        hourly_soil_temperature_0cm = hourly.Variables(33).ValuesAsNumpy()
        hourly_soil_temperature_6cm = hourly.Variables(34).ValuesAsNumpy()
        hourly_soil_temperature_18cm = hourly.Variables(35).ValuesAsNumpy()
        hourly_soil_temperature_54cm = hourly.Variables(36).ValuesAsNumpy()
        hourly_soil_moisture_0_to_1cm = hourly.Variables(37).ValuesAsNumpy()
        hourly_soil_moisture_1_to_3cm = hourly.Variables(38).ValuesAsNumpy()
        hourly_soil_moisture_3_to_9cm = hourly.Variables(39).ValuesAsNumpy()
        hourly_soil_moisture_9_to_27cm = hourly.Variables(40).ValuesAsNumpy()
        hourly_soil_moisture_27_to_81cm = hourly.Variables(41).ValuesAsNumpy()

        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ),
            "temperature_2m": hourly_temperature_2m,
            "relative_humidity_2m": hourly_relative_humidity_2m,
            "dew_point_2m": hourly_dew_point_2m,
            "apparent_temperature": hourly_apparent_temperature,
            "precipitation_probability": hourly_precipitation_probability,
            "precipitation": hourly_precipitation,
            "rain": hourly_rain,
            "showers": hourly_showers,
            "snow_depth": hourly_snow_depth,
            "snowfall": hourly_snowfall,
            "weather_code": hourly_weather_code,
            "surface_pressure": hourly_surface_pressure,
            "pressure_msl": hourly_pressure_msl,
            "cloud_cover": hourly_cloud_cover,
            "cloud_cover_low": hourly_cloud_cover_low,
            "cloud_cover_mid": hourly_cloud_cover_mid,
            "cloud_cover_high": hourly_cloud_cover_high,
            "visibility": hourly_visibility,
            "evapotranspiration": hourly_evapotranspiration,
            "et0_fao_evapotranspiration": hourly_et0_fao_evapotranspiration,
            "vapour_pressure_deficit": hourly_vapour_pressure_deficit,
            "wind_speed_10m": hourly_wind_speed_10m,
            "wind_speed_80m": hourly_wind_speed_80m,
            "wind_speed_120m": hourly_wind_speed_120m,
            "wind_speed_180m": hourly_wind_speed_180m,
            "wind_direction_10m": hourly_wind_direction_10m,
            "wind_direction_80m": hourly_wind_direction_80m,
            "wind_direction_180m": hourly_wind_direction_180m,
            "wind_direction_120m": hourly_wind_direction_120m,
            "wind_gusts_10m": hourly_wind_gusts_10m,
            "temperature_80m": hourly_temperature_80m,
            "temperature_120m": hourly_temperature_120m,
            "temperature_180m": hourly_temperature_180m,
            "soil_temperature_0cm": hourly_soil_temperature_0cm,
            "soil_temperature_6cm": hourly_soil_temperature_6cm,
            "soil_temperature_18cm": hourly_soil_temperature_18cm,
            "soil_temperature_54cm": hourly_soil_temperature_54cm,
            "soil_moisture_0_to_1cm": hourly_soil_moisture_0_to_1cm,
            "soil_moisture_1_to_3cm": hourly_soil_moisture_1_to_3cm,
            "soil_moisture_3_to_9cm": hourly_soil_moisture_3_to_9cm,
            "soil_moisture_9_to_27cm": hourly_soil_moisture_9_to_27cm,
            "soil_moisture_27_to_81cm": hourly_soil_moisture_27_to_81cm,
        }

        hourly_dataframe = pd.DataFrame(data=hourly_data)
        logger.info(f"Stundendaten: {len(hourly_dataframe)} Einträge")

        # ===== DAILY DATA =====
        logger.info("Verarbeite tägliche Daten...")
        daily = response.Daily()

        daily_weather_code = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
        daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()
        daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()
        daily_sunrise = daily.Variables(5).ValuesInt64AsNumpy()
        daily_sunset = daily.Variables(6).ValuesInt64AsNumpy()
        daily_daylight_duration = daily.Variables(7).ValuesAsNumpy()
        daily_sunshine_duration = daily.Variables(8).ValuesAsNumpy()
        daily_uv_index_max = daily.Variables(9).ValuesAsNumpy()
        daily_uv_index_clear_sky_max = daily.Variables(10).ValuesAsNumpy()
        daily_rain_sum = daily.Variables(11).ValuesAsNumpy()
        daily_showers_sum = daily.Variables(12).ValuesAsNumpy()
        daily_snowfall_sum = daily.Variables(13).ValuesAsNumpy()
        daily_precipitation_sum = daily.Variables(14).ValuesAsNumpy()
        daily_precipitation_hours = daily.Variables(15).ValuesAsNumpy()
        daily_precipitation_probability_max = daily.Variables(16).ValuesAsNumpy()
        daily_wind_speed_10m_max = daily.Variables(17).ValuesAsNumpy()
        daily_wind_gusts_10m_max = daily.Variables(18).ValuesAsNumpy()
        daily_shortwave_radiation_sum = daily.Variables(19).ValuesAsNumpy()
        daily_wind_direction_10m_dominant = daily.Variables(20).ValuesAsNumpy()
        daily_et0_fao_evapotranspiration = daily.Variables(21).ValuesAsNumpy()

        daily_data = {
            "date": pd.date_range(
                start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=daily.Interval()),
                inclusive="left"
            ),
            "weather_code": daily_weather_code,
            "temperature_2m_max": daily_temperature_2m_max,
            "temperature_2m_min": daily_temperature_2m_min,
            "apparent_temperature_max": daily_apparent_temperature_max,
            "apparent_temperature_min": daily_apparent_temperature_min,
            "sunrise": pd.to_datetime(daily_sunrise, unit="s", utc=True),
            "sunset": pd.to_datetime(daily_sunset, unit="s", utc=True),
            "daylight_duration": daily_daylight_duration,
            "sunshine_duration": daily_sunshine_duration,
            "uv_index_max": daily_uv_index_max,
            "uv_index_clear_sky_max": daily_uv_index_clear_sky_max,
            "rain_sum": daily_rain_sum,
            "showers_sum": daily_showers_sum,
            "snowfall_sum": daily_snowfall_sum,
            "precipitation_sum": daily_precipitation_sum,
            "precipitation_hours": daily_precipitation_hours,
            "precipitation_probability_max": daily_precipitation_probability_max,
            "wind_speed_10m_max": daily_wind_speed_10m_max,
            "wind_gusts_10m_max": daily_wind_gusts_10m_max,
            "shortwave_radiation_sum": daily_shortwave_radiation_sum,
            "wind_direction_10m_dominant": daily_wind_direction_10m_dominant,
            "et0_fao_evapotranspiration": daily_et0_fao_evapotranspiration,
        }

        daily_dataframe = pd.DataFrame(data=daily_data)
        logger.info(f"Tageswerte: {len(daily_dataframe)} Einträge")

        # ===== SPEICHERN =====
        logger.info("Speichere Daten in Datenbank...")
        insert_weather_data(
            connection_string=connection_string,
            latitude=latitude,
            longitude=longitude,
            current_data=current_dict,
            hourly_df=hourly_dataframe,
            daily_df=daily_dataframe
        )

        logger.info(f"✓ Location {latitude}, {longitude} erfolgreich verarbeitet")
        time.sleep(2)

    except Exception as e:
        logger.error(f"✗ Fehler bei Location {latitude}, {longitude}: {str(e)}", exc_info=True)
        continue

logger.info("=" * 80)
logger.info("Alle Wetterdaten erfolgreich in die Datenbank gespeichert!")
logger.info("=" * 80)
