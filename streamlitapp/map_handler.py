"""
Kartenfunktionen und Wetter-Overlay für Leaflet
"""
import streamlit as st
import streamlit.components.v1 as components
from api_client import fetch_weather_data


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
            
            temp_value = current_data.get("temperature_2m", 0)
            weather_code = int(current_data.get("weather_code", 0))
            
            cities_weather.append({
                "name": city["name"],
                "lat": city["lat"],
                "lon": city["lon"],
                "temperature": round(float(temp_value), 1),
                "weather_code": weather_code,
                "weather_emoji": get_weather_emoji(weather_code),
                "cloud_cover": round(float(current_data.get("cloud_cover", 0)), 0),
                "wind_speed": round(float(current_data.get("wind_speed_10m", 0)), 1),
                "humidity": round(float(current_data.get("relative_humidity_2m", 0)), 0),
            })
        except Exception as e:
            # Fallback: Zeige Ort ohne Fehlermeldung
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
    
    return cities_weather


def create_weather_map(cities_weather: list = None, map_height: int = 500) -> str:
    """
    Erstellt ein Leaflet-HTML-String mit Wetter-Markern basierend auf dem Original-Template.
    
    Args:
        cities_weather: Liste mit Wetterdaten für Städte
        map_height: Höhe der Karte in Pixeln
        
    Returns:
        HTML-String für Leaflet-Karte
    """
    # Falls keine Daten vorhanden, Standarddaten verwenden
    if not cities_weather or len(cities_weather) == 0:
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
    
    # Erstelle JavaScript-Marker-Array
    markers_js = "["
    for i, city in enumerate(cities_weather):
        color = get_weather_color(city["weather_code"])
        temp_str = str(city["temperature"]) if city["temperature"] != "--" else "--"
        emoji = city["weather_emoji"]
        
        popup_content = f"""<div style="text-align: center; font-family: Arial, sans-serif; padding: 10px; width: 200px;">
                <div style="font-weight: bold; font-size: 16px; margin-bottom: 5px;">{city['name']}</div>
                <div style="font-size: 32px; margin: 10px 0;">{emoji}</div>
                <div style="font-size: 24px; font-weight: bold; color: #FF6B6B; margin: 8px 0;">
                    {temp_str}°C
                </div>
                <hr style="margin: 10px 0; border: none; border-top: 1px solid #ddd;">
                <div style="font-size: 12px; text-align: left;">
                    <div>☁️ Bewölkung: {city['cloud_cover']}%</div>
                    <div>💧 Feuchte: {city['humidity']}%</div>
                    <div>💨 Wind: {city['wind_speed']} km/h</div>
                </div>
            </div>"""
        
        markers_js += f"""
        {{
            lat: {city['lat']},
            lon: {city['lon']},
            name: '{city['name']}',
            temp: '{temp_str}',
            emoji: '{emoji}',
            color: '{color}',
            popup: '{popup_content.replace(chr(10), " ").replace(chr(39), "\\\'")}',
            cloud: {city['cloud_cover'] if isinstance(city['cloud_cover'], int) else 0},
            humidity: {city['humidity'] if isinstance(city['humidity'], int) else 0},
            wind: {city['wind_speed'] if isinstance(city['wind_speed'], (int, float)) else 0}
        }}"""
        if i < len(cities_weather) - 1:
            markers_js += ","
    markers_js += "]"
    
    # HTML mit Leaflet-Karte basierend auf Original-Template
    leaflet_html = f"""
    <div id="map" style="width: 100%; height: {map_height}px;"></div>

    <!-- Leaflet CSS & JS -->
    <link
      rel="stylesheet"
      href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

    <script>
      // Bounds für Schweiz-Ausschnitt
      var bounds = L.latLngBounds(
        L.latLng(45.5, 5.5),   // Süd-West
        L.latLng(48.0, 11.0)   // Nord-Ost
      );

      // Karte auf diese Bounds zoomen und begrenzen
      var map = L.map('map', {{
        maxBounds: bounds,
        maxBoundsViscosity: 1.0
      }}).fitBounds(bounds);

      // Basiskarte (OSM)
      L.tileLayer(
        'https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',
        {{
          maxZoom: 14,
          minZoom: 6
        }}
      ).addTo(map);

      // Rahmen um die Schweiz
      L.rectangle(bounds, {{
        color: "#00aaff",
        weight: 1,
        fillOpacity: 0.0
      }}).addTo(map);

      // Wetter-Marker hinzufügen
      var weatherData = {markers_js};
      
      weatherData.forEach(function(marker) {{
        L.circleMarker([marker.lat, marker.lon], {{
          radius: 25,
          fillColor: marker.color,
          color: '#333',
          weight: 2,
          opacity: 0.9,
          fillOpacity: 0.85
        }}).bindPopup(marker.popup).addTo(map);
      }});
    </script>
    """
    
    return leaflet_html


def display_weather_map(show_loading: bool = True, map_height: int = 500):
    """
    Zeigt die Wetter-Karte in Streamlit an mit oder ohne Loader.
    
    Args:
        show_loading: Zeige Lade-Spinner
        map_height: Höhe der Karte in Pixeln (default 500)
    """
    try:
        # Versuche Wetterdaten zu laden
        if show_loading:
            with st.spinner("⏳ Lade Wetterdaten für alle Städte..."):
                cities_weather = fetch_city_weather_data()
        else:
            cities_weather = fetch_city_weather_data()
        
        # Erstelle HTML und zeige Karte
        map_html = create_weather_map(cities_weather, map_height)
        components.html(map_html, height=map_height + 50, scrolling=False)
        
    except Exception as e:
        # Fallback: Zeige Standard-Karte ohne Daten
        st.warning(f"⚠️ Konnte Wetterdaten nicht laden: {str(e)}")
        st.info("Die Karte wird mit Standarddaten angezeigt...")
        
        try:
            map_html = create_weather_map(None, map_height)
            components.html(map_html, height=map_height + 50, scrolling=False)
        except Exception as e2:
            st.error(f"❌ Fehler beim Laden der Karte: {str(e2)}")

