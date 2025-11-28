pfad = ".\locaction_cantons.csv"

pfad = "C:\\Users\\rki\\Git\\smart-weather.ch_semesterrarbeit02\\scripts\\locaction_cantons.csv"

import csv
import requests
import json
import psycopg
from typing import List

location_registry = []

class Location:
    def __init__(self, name, canton, latitude, longitude, elevation, feature_code):
        self.name = name
        self.canton = canton
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.feature_code = feature_code

    def __str__(self):
        return f"Location: {self.name} | Canton: {self.canton} | Elev: {self.elevation} | Lat: {self.latitude} | Lon: {self.longitude} | Feature Code: {self.feature_code}"
    

def get_csv_data_minimal(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8-sig') as file:
        data_reader = csv.DictReader(file, delimiter=';')
        content = list(data_reader)
        header = data_reader.fieldnames 
    return header, content


locationData = get_csv_data_minimal(pfad)

locationData

locationValues = locationData[1]

for locName in locationValues:
    print(f"{locName.get('Ort')} ist in Kanton {locName.get('Kanton')}") 

    api_url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
           "name": locName.get('Ort'), 
           "count": 1,
           "language": "en",
           "format": "json",
           "countryCode": "CH"
       }

    response = requests.get(api_url, params=params)
    
    data = response.json()
    results = data.get('results', []) 
    
    if results:
        item = results[0]
    
    # Create a new Location object using data from the API and CSV
    new_location = Location(
        name=item.get('name'),
        canton=locName.get('Kanton'), 
        latitude=item.get('latitude'),
        longitude=item.get('longitude'),
        elevation=item.get('elevation'),
        feature_code=item.get('feature_code')
    )
    
    location_registry.append(new_location)
    print(f"Successfully added {new_location.name}.")

DB_HOST = "host.smart-ch.ch"    
DB_NAME = "smartweatherdb" 
DB_USER = "dbadm_robin"
DB_PASSWORD = "xxxxx"
DB_PORT = "5432"      

connection_string = f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} port={DB_PORT}"
with psycopg.connect(connection_string) as conn:
    with conn.cursor() as cur:
        for location in location_registry:
            cur.execute(
                """
                INSERT INTO geo_location
                    (name, canton, latitude, longitude, elevation, feature_code)
                VALUES
                    (%s, %s, %s, %s, %s, %s)
                ON CONFLICT ON CONSTRAINT geo_location_lat_lon_uniq
                DO NOTHING;
                """,
                (
                    location.name,
                    location.canton,
                    location.latitude,
                    location.longitude,
                    location.elevation,
                    location.feature_code,
                )
            )
    conn.commit()

