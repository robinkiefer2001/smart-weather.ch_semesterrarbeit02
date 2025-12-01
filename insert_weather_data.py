import psycopg
import pandas as pd
from datetime import datetime, timezone
import logging

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def insert_weather_data(
    connection_string: str,
    latitude: float,
    longitude: float,
    current_data: dict,
    hourly_df: pd.DataFrame,
    daily_df: pd.DataFrame
):
    """
    Speichert Wetterdaten aus Open-Meteo API in die PostgreSQL Datenbank.
    
    Diese Funktion:
    - Speichert aktuelle Wetterdaten in weather_current
    - Speichert stündliche Daten in weather_hourly (bis zu 672 Stunden)
    - Speichert tägliche Daten in weather_daily (bis zu 28 Tage)
    
    Bei Duplikaten (gleiche Koordinaten + Zeit) wird nichts eingefügt (ON CONFLICT DO NOTHING).
    
    Args:
        connection_string: PostgreSQL Verbindungsstring
        latitude: Breitengrad (DECIMAL(9,6))
        longitude: Längengrad (DECIMAL(9,6))
        current_data: Dict mit aktuellen Wettervariablen
        hourly_df: Pandas DataFrame mit Stundendaten (Spalte 'date' muss TIMESTAMPTZ sein)
        daily_df: Pandas DataFrame mit Tageswerten (Spalte 'date' muss DATE sein)
    
    Raises:
        psycopg.Error: Bei Datenbankfehlern
        ValueError: Bei ungültigen Eingabedaten
    """
    
    with psycopg.connect(connection_string) as conn:
        with conn.cursor() as cur:
            
            # ===== 1. CURRENT DATA =====
            logger.info(f"Speichere aktuelle Daten für ({latitude}, {longitude})")
            
            sql_current = """
                INSERT INTO weather_current (
                    latitude, longitude, observed_at,
                    temperature_2m, relative_humidity_2m, apparent_temperature,
                    is_day, precipitation, rain, showers, snowfall,
                    weather_code, cloud_cover, pressure_msl, surface_pressure,
                    wind_speed_10m, wind_direction_10m, wind_gusts_10m
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (latitude, longitude, observed_at) DO NOTHING;
            """
            
            # Timestamp konvertieren (Unix Timestamp zu DateTime UTC)
            observed_at = datetime.fromtimestamp(current_data['time'], tz=timezone.utc)
            
            cur.execute(sql_current, (
                latitude, longitude, observed_at,
                current_data.get('temperature_2m'),
                current_data.get('relative_humidity_2m'),
                current_data.get('apparent_temperature'),
                bool(current_data.get('is_day')),
                current_data.get('precipitation'),
                current_data.get('rain'),
                current_data.get('showers'),
                current_data.get('snowfall'),
                current_data.get('weather_code'),
                current_data.get('cloud_cover'),
                current_data.get('pressure_msl'),
                current_data.get('surface_pressure'),
                current_data.get('wind_speed_10m'),
                current_data.get('wind_direction_10m'),
                current_data.get('wind_gusts_10m')
            ))
            
            logger.info(f"✓ Current-Daten eingefügt")
            
            # ===== 2. HOURLY DATA =====
            logger.info(f"Speichere {len(hourly_df)} Stundendaten")
            
            # Füge lat/lon zu DataFrame hinzu
            hourly_df_insert = hourly_df.copy()
            hourly_df_insert['latitude'] = latitude
            hourly_df_insert['longitude'] = longitude
            
            # Spaltenreihenfolge muss mit SQL-Statement übereinstimmen!
            hourly_cols = [
                'latitude', 'longitude', 'date',
                'temperature_2m', 'relative_humidity_2m', 'dew_point_2m',
                'apparent_temperature', 'precipitation_probability', 'precipitation',
                'rain', 'showers', 'snow_depth', 'snowfall', 'weather_code',
                'surface_pressure', 'pressure_msl', 'cloud_cover',
                'cloud_cover_low', 'cloud_cover_mid', 'cloud_cover_high',
                'visibility', 'evapotranspiration', 'et0_fao_evapotranspiration',
                'vapour_pressure_deficit', 'wind_speed_10m', 'wind_speed_80m',
                'wind_speed_120m', 'wind_speed_180m', 'wind_direction_10m',
                'wind_direction_80m', 'wind_direction_120m', 'wind_direction_180m',
                'wind_gusts_10m', 'temperature_80m', 'temperature_120m',
                'temperature_180m', 'soil_temperature_0cm', 'soil_temperature_6cm',
                'soil_temperature_18cm', 'soil_temperature_54cm',
                'soil_moisture_0_to_1cm', 'soil_moisture_1_to_3cm',
                'soil_moisture_3_to_9cm', 'soil_moisture_9_to_27cm',
                'soil_moisture_27_to_81cm'
            ]
            
            # Nur Spalten auswählen, die im DF vorhanden sind
            available_cols = [col for col in hourly_cols if col in hourly_df_insert.columns]
            hourly_records = hourly_df_insert[available_cols].values.tolist()
            
            sql_hourly = """
                INSERT INTO weather_hourly (
                    latitude, longitude, observed_at,
                    temperature_2m, relative_humidity_2m, dew_point_2m,
                    apparent_temperature, precipitation_probability, precipitation,
                    rain, showers, snow_depth, snowfall, weather_code,
                    surface_pressure, pressure_msl, cloud_cover,
                    cloud_cover_low, cloud_cover_mid, cloud_cover_high,
                    visibility, evapotranspiration, et0_fao_evapotranspiration,
                    vapour_pressure_deficit, wind_speed_10m, wind_speed_80m,
                    wind_speed_120m, wind_speed_180m, wind_direction_10m,
                    wind_direction_80m, wind_direction_120m, wind_direction_180m,
                    wind_gusts_10m, temperature_80m, temperature_120m,
                    temperature_180m, soil_temperature_0cm, soil_temperature_6cm,
                    soil_temperature_18cm, soil_temperature_54cm,
                    soil_moisture_0_to_1cm, soil_moisture_1_to_3cm,
                    soil_moisture_3_to_9cm, soil_moisture_9_to_27cm,
                    soil_moisture_27_to_81cm
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (latitude, longitude, observed_at) DO NOTHING;
            """
            
            cur.executemany(sql_hourly, hourly_records)
            logger.info(f"✓ {len(hourly_records)} Stundendaten eingefügt")
            
            # ===== 3. DAILY DATA =====
            logger.info(f"Speichere {len(daily_df)} Tageswerte")
            
            daily_df_insert = daily_df.copy()
            daily_df_insert['latitude'] = latitude
            daily_df_insert['longitude'] = longitude
            
            daily_cols = [
                'latitude', 'longitude', 'date',
                'weather_code', 'temperature_2m_max', 'temperature_2m_min',
                'apparent_temperature_max', 'apparent_temperature_min',
                'sunrise', 'sunset', 'daylight_duration', 'sunshine_duration',
                'uv_index_max', 'uv_index_clear_sky_max', 'rain_sum', 'showers_sum',
                'snowfall_sum', 'precipitation_sum', 'precipitation_hours',
                'precipitation_probability_max', 'wind_speed_10m_max',
                'wind_gusts_10m_max', 'shortwave_radiation_sum',
                'wind_direction_10m_dominant', 'et0_fao_evapotranspiration'
            ]
            
            available_daily_cols = [col for col in daily_cols if col in daily_df_insert.columns]
            daily_records = daily_df_insert[available_daily_cols].values.tolist()
            
            sql_daily = """
                INSERT INTO weather_daily (
                    latitude, longitude, day,
                    weather_code, temperature_2m_max, temperature_2m_min,
                    apparent_temperature_max, apparent_temperature_min,
                    sunrise, sunset, daylight_duration, sunshine_duration,
                    uv_index_max, uv_index_clear_sky_max, rain_sum, showers_sum,
                    snowfall_sum, precipitation_sum, precipitation_hours,
                    precipitation_probability_max, wind_speed_10m_max,
                    wind_gusts_10m_max, shortwave_radiation_sum,
                    wind_direction_10m_dominant, et0_fao_evapotranspiration
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (latitude, longitude, day) DO NOTHING;
            """
            
            cur.executemany(sql_daily, daily_records)
            logger.info(f"✓ {len(daily_records)} Tageswerte eingefügt")
            
            # Transaktion abschliessen
            conn.commit()
            logger.info(f"✓✓✓ Alle Daten für ({latitude}, {longitude}) erfolgreich gespeichert")
