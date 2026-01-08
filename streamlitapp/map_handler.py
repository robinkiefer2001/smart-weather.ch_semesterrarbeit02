"""
Kartenfunktionen und Wetter-Overlay für Leaflet
"""
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from api_client import fetch_weather_data
from database import search_location
import json


# Hauptstädte und wichtige Orte in der Schweiz
MAJOR_CITIES = [
    {"name": "Zürich", "lat": 47.3769, "lon": 8.5472},
    {"name": "Bern", "lat": 46.9479, "lon": 7.4474},
    {"name": "Basel", "lat": 47.5596, "lon": 7.5886},
    {"name": "Genf", "lat": 46.2044, "lon": 6.1432},
    {"name": "Lausanne", "lat": 46.5197, "lon": 6.6323},
    {"name": "Luzern", "lat": 47.0502, "lon": 8.3093},
    {"name": "St. Gallen", "lat": 47.4229, "lon": 9.3767},
    {"name": "Lugano", "lat": 46.0051, "lon": 8.9511},
    {"name": "Winterthur", "lat": 47.5034, "lon": 8.7519},
    {"name": "Biel", "lat": 47.1390, "lon": 7.2458},
    {"name": "Neuenburg", "lat": 46.9920, "lon": 6.9282},
    {"name": "Montreux", "lat": 46.4335, "lon": 6.9148},
    {"name": "Sion", "lat": 46.2206, "lon": 7.5605},
    {"name": "Interlaken", "lat": 46.6863, "lon": 8.1659},
    {"name": "Appenzell", "lat": 47.3310, "lon": 9.4151},
]


def get_weather_emoji(weather_code: int) -> str:
    """
    Konvertiert Weather Code zu Emoji für Kartendarstellung.
    """
    weather_emojis = {
        0: "☀️",    # Klar
        1: "🌤️",   # Teilweise bewölkt
        2: "⛅",    # Bewölkt
        3: "☁️",    # Bedeckt
        45: "🌫️",   # Nebel
        48: "🌫️",   # Gefrierender Nebel
        51: "🌦️",   # Leichter Nieselregen
        53: "🌧️",   # Mäßiger Nieselregen
        55: "🌧️",   # Starker Nieselregen
        61: "🌧️",   # Leichter Regen
        63: "🌧️",   # Mäßiger Regen
        65: "🌧️",   # Starker Regen
        71: "❄️",    # Leichter Schneefall
        73: "❄️",    # Mäßiger Schneefall
        75: "❄️",    # Starker Schneefall
        80: "🌦️",   # Leichte Regenschauer
        81: "🌧️",   # Mäßige Regenschauer
        82: "🌧️",   # Starke Regenschauer
        95: "⛈️",   # Gewitter
        99: "⛈️",   # Schweres Gewitter mit Hagel
    }
    return weather_emojis.get(weather_code, "❓")


def get_weather_color(weather_code: int) -> str:
    """
    Gibt eine Farbe basierend auf Wetterbedingung zurück.
    """
    if weather_code == 0:
        return "#FFD700"  # Gold für sonnig
    elif weather_code in [1, 2]:
        return "#87CEEB"  # Sky blue für bewölkt
    elif weather_code in [3]:
        return "#808080"  # Grau für bedeckt
    elif weather_code in [45, 48]:
        return "#A9A9A9"  # Dunkelgrau für Nebel
    elif weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
        return "#4169E1"  # Royal blue für Regen
    elif weather_code in [71, 73, 75]:
        return "#F0F8FF"  # Alice blue für Schnee
    elif weather_code in [95, 99]:
        return "#FF6347"  # Tomato rot für Gewitter
    else:
        return "#808080"  # Default grau


def fetch_city_weather_data() -> list:
    """
    Holt Wetterdaten für alle Hauptstädte.
    
    Returns:
        Liste mit Wetterdaten für jede Stadt
    """
    cities_weather = []
    
    for city in MAJOR_CITIES:
        try:
            current_data, _, _ = fetch_weather_data(city["lat"], city["lon"])
            
            cities_weather.append({
                "name": city["name"],
                "lat": city["lat"],
                "lon": city["lon"],
                "temperature": current_data["temperature_2m"],
                "weather_code": int(current_data["weather_code"]),
                "weather_emoji": get_weather_emoji(int(current_data["weather_code"])),
                "cloud_cover": current_data["cloud_cover"],
                "wind_speed": current_data["wind_speed_10m"],
                "humidity": current_data["relative_humidity_2m"],
            })
        except Exception as e:
            st.warning(f"Fehler beim Abrufen von Daten für {city['name']}: {str(e)}")
            # Fallback mit leeren Daten
            cities_weather.append({
                "name": city["name"],
                "lat": city["lat"],
                "lon": city["lon"],
                "temperature": "N/A",
                "weather_code": 0,
                "weather_emoji": "❓",
                "cloud_cover": "N/A",
                "wind_speed": "N/A",
                "humidity": "N/A",
            })
    
    return cities_weather


def create_weather_map(cities_weather: list = None) -> str:
    """
    Erstellt ein Leaflet-HTML-String mit Wetter-Markern.
    
    Args:
        cities_weather: Liste mit Wetterdaten für Städte
        
    Returns:
        HTML-String für Leaflet-Karte
    """
    # Falls keine Daten vorhanden, Standarddaten verwenden
    if cities_weather is None:
        cities_weather = []
        for city in MAJOR_CITIES:
            cities_weather.append({
                "name": city["name"],
                "lat": city["lat"],
                "lon": city["lon"],
                "temperature": "--",
                "weather_code": 0,
                "weather_emoji": "❓",
                "cloud_cover": "--",
                "wind_speed": "--",
                "humidity": "--",
            })
    
    # Erstelle GeoJSON-Feature für jeden Ort
    features = []
    for city in cities_weather:
        color = get_weather_color(city["weather_code"])
        
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [city["lon"], city["lat"]]
            },
            "properties": {
                "name": city["name"],
                "temperature": city["temperature"],
                "weather_emoji": city["weather_emoji"],
                "cloud_cover": city["cloud_cover"],
                "wind_speed": city["wind_speed"],
                "humidity": city["humidity"],
                "color": color
            }
        }
        features.append(feature)
    
    geojson_data = json.dumps({
        "type": "FeatureCollection",
        "features": features
    })
    
    # HTML mit Leaflet-Karte
    leaflet_html = f"""
    <div id="map" style="width: 100%; height: 700px; position: relative;"></div>
    
    <!-- Leaflet CSS & JS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    
    <!-- Font Awesome für bessere Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
    
    <script>
        // Bounds für Schweiz-Ausschnitt
        var bounds = L.latLngBounds(
            L.latLng(45.5, 5.5),   // Süd-West
            L.latLng(48.0, 11.0)   // Nord-Ost
        );
        
        // Karte initialisieren
        var map = L.map('map', {{
            maxBounds: bounds,
            maxBoundsViscosity: 1.0
        }}).fitBounds(bounds);
        
        // OpenStreetMap Layer
        L.tileLayer(
            'https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',
            {{
                maxZoom: 14,
                minZoom: 6,
                attribution: '© OpenStreetMap contributors'
            }}
        ).addTo(map);
        
        // GeoJSON Daten
        var geojsonData = {geojson_data};
        
        // Custom CircleMarker mit Wetter-Info
        L.geoJSON(geojsonData, {{
            pointToLayer: function(feature, latlng) {{
                var props = feature.properties;
                
                // Bestimme Icon-Größe basierend auf Temperatur
                var size = 50;
                
                // Erstelle einen Container für die Anzeige
                var popupContent = `
                    <div style="text-align: center; font-family: Arial, sans-serif; padding: 10px;">
                        <div style="font-weight: bold; font-size: 16px; margin-bottom: 5px;">${{props.name}}</div>
                        <div style="font-size: 32px; margin: 10px 0;">${{props.weather_emoji}}</div>
                        <div style="font-size: 24px; font-weight: bold; color: #FF6B6B; margin: 8px 0;">
                            ${{props.temperature}}°C
                        </div>
                        <hr style="margin: 10px 0; border: none; border-top: 1px solid #ddd;">
                        <div style="font-size: 12px; text-align: left;">
                            <div>☁️ Bewölkung: ${{props.cloud_cover}}%</div>
                            <div>💧 Feuchte: ${{props.humidity}}%</div>
                            <div>💨 Wind: ${{props.wind_speed}} km/h</div>
                        </div>
                    </div>
                `;
                
                // Erstelle einen farbigen Kreis mit Emoji
                return L.circleMarker(latlng, {{
                    radius: 25,
                    fillColor: props.color,
                    color: '#333',
                    weight: 2,
                    opacity: 0.9,
                    fillOpacity: 0.85
                }}).bindPopup(popupContent, {{
                    maxWidth: 250,
                    className: 'weather-popup'
                }});
            }}
        }}).addTo(map);
        
        // Rechteck-Rahmen um die Schweiz
        L.rectangle(bounds, {{
            color: "#00aaff",
            weight: 2,
            fillOpacity: 0.0
        }}).addTo(map);
    </script>
    
    <style>
        .weather-popup .leaflet-popup-content-wrapper {{
            background-color: #f9f9f9;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }}
        
        .weather-popup .leaflet-popup-tip {{
            background-color: #f9f9f9;
        }}
    </style>
    """
    
    return leaflet_html


def display_weather_map(show_loading: bool = True):
    """
    Zeigt die Wetter-Karte in Streamlit an mit oder ohne Loader.
    
    Args:
        show_loading: Zeige Lade-Spinner
    """
    if show_loading:
        with st.spinner("⏳ Lade Wetterdaten für alle Städte..."):
            cities_weather = fetch_city_weather_data()
    else:
        cities_weather = fetch_city_weather_data()
    
    map_html = create_weather_map(cities_weather)
    components.html(map_html, height=750, scrolling=False)
