"""
Kartenfunktionen und Wetter-Overlay für Leaflet
"""
import streamlit as st
from api_client import fetch_weather_data
import time


@st.cache_data(ttl=300)  # Cache für 5 Minuten
def get_cached_weather_data(lat: float, lon: float) -> dict:
    """
    Holt gecachte Wetterdaten für eine Stadt.
    TTL: 5 Minuten
    """
    try:
        current_data, _, _ = fetch_weather_data(lat, lon)
        return {
            "success": True,
            "data": current_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# Hauptstädte und wichtige Orte in der Schweiz - reduziert auf Regionen
MAJOR_CITIES = [
    {"name": "Zürich", "lat": 47.3769, "lon": 8.5472, "region": "Nordost"},
    {"name": "Bern", "lat": 46.9479, "lon": 7.4474, "region": "Mitte"},
    {"name": "Basel", "lat": 47.5596, "lon": 7.5886, "region": "Nordwest"},
    {"name": "Genf", "lat": 46.2044, "lon": 6.1432, "region": "Westen"},
    {"name": "Lausanne", "lat": 46.5197, "lon": 6.6323, "region": "Westen"},
    {"name": "Luzern", "lat": 47.0502, "lon": 8.3093, "region": "Zentralschweiz"},
    {"name": "Lugano", "lat": 46.0051, "lon": 8.9511, "region": "Tessin"},
    {"name": "Chur", "lat": 46.8519, "lon": 9.5322, "region": "Graubünden"},
    {"name": "Schaffhausen", "lat": 47.6965, "lon": 8.6361, "region": "Nordost"},
    {"name": "Sitten", "lat": 46.2906, "lon": 7.6050, "region": "Süden"},
    {"name": "Zug", "lat": 47.1645, "lon": 8.5169, "region": "Zentralschweiz"},
    {"name": "St. Gallen", "lat": 47.4229, "lon": 9.3767, "region": "Ostschweiz"},
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
    Holt Wetterdaten für alle Hauptstädte mit Rate-Limiting und Fehlerbehandlung.
    Verwendet Caching um API-Limits zu respektieren.
    
    Returns:
        Liste mit Wetterdaten für jede Stadt
    """
    cities_weather = []
    
    for i, city in enumerate(MAJOR_CITIES):
        try:
            # Rate-Limiting: Kleine Verzögerung zwischen Anfragen
            if i > 0:
                time.sleep(0.2)  # 200ms Verzögerung zwischen Anfragen
            
            # Versuche gecachte Daten zu holen
            weather_result = get_cached_weather_data(city["lat"], city["lon"])
            
            if weather_result["success"]:
                current_data = weather_result["data"]
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
            else:
                # Bei Fehler: Fallback mit Standarddaten
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


def create_weather_map(cities_weather: list = None, search_location: dict = None, map_height: int = 500) -> str:
    """
    Erstellt ein Leaflet-HTML-String mit Wetter-Markern basierend auf dem Original-Template.
    
    Args:
        cities_weather: Liste mit Wetterdaten für Städte
        search_location: Dict mit {"name": str, "lat": float, "lon": float} der gesuchten Location
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
    
    # Erstelle Marker-Daten als JavaScript Array
    markers_code = "var markers = [\n"
    for i, city in enumerate(cities_weather):
        color = get_weather_color(city["weather_code"])
        temp_str = str(city["temperature"]) if city["temperature"] != "--" else "--"
        emoji = city["weather_emoji"]
        
        # Escape HTML-Zeichen für JavaScript
        popup_html = f"""<div style="text-align: center; font-family: Arial, sans-serif; padding: 10px;">
<strong>{city['name']}</strong><br>
<div style="font-size: 32px;">{emoji}</div>
<strong style="color: #FF6B6B; font-size: 20px;">{temp_str}°C</strong><br>
<small>☁️ {city['cloud_cover']}% | 💧 {city['humidity']}% | 💨 {city['wind_speed']} km/h</small>
</div>"""
        
        # Escape für JavaScript
        popup_escaped = popup_html.replace("'", "\\'").replace("\n", " ")
        
        markers_code += f"""  {{
    lat: {city['lat']},
    lon: {city['lon']},
    name: '{city['name']}',
    popup: '{popup_escaped}',
    color: '{color}',
    type: 'city'
  }}"""
        if i < len(cities_weather) - 1:
            markers_code += ","
        markers_code += "\n"
    
    # Füge gesuchte Location hinzu, wenn vorhanden
    if search_location:
        search_popup = f'<div style="text-align: center; font-family: Arial, sans-serif; padding: 10px;"><strong style="color: #FF6B6B; font-size: 18px;">📍 {search_location["name"]}</strong><br><small>Gesuchter Ort</small></div>'
        search_popup_escaped = search_popup.replace("'", "\\'").replace("\n", " ")
        markers_code += f""",
  {{
    lat: {search_location['lat']},
    lon: {search_location['lon']},
    name: '{search_location['name']} 📍',
    popup: '{search_popup_escaped}',
    color: '#FF0000',
    type: 'search'
  }}"""
    
    markers_code += "];"
    
    # HTML mit Leaflet-Karte
    leaflet_html = f"""
    <div id="map" style="width: 100%; height: {map_height}px;"></div>

    <!-- Leaflet CSS & JS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
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

      // Marker-Daten
      {markers_code}
      
      // Marker hinzufügen
      markers.forEach(function(markerData) {{
        var markerSize = markerData.type === 'search' ? 30 : 25;
        var borderColor = markerData.type === 'search' ? '#000000' : '#333';
        var borderWeight = markerData.type === 'search' ? 3 : 2;
        
        L.circleMarker([markerData.lat, markerData.lon], {
          radius: markerSize,
          fillColor: markerData.color,
          color: borderColor,
          weight: borderWeight,
          opacity: 0.95,
          fillOpacity: markerData.type === 'search' ? 0.7 : 0.85
        }}).bindPopup(markerData.popup).addTo(map);
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
        st.html(map_html)
        
    except Exception as e:
        # Fallback: Zeige Standard-Karte ohne Daten
        st.warning(f"⚠️ Konnte Wetterdaten nicht laden: {str(e)}")
        st.info("Die Karte wird mit Standarddaten angezeigt...")
        
        try:
            map_html = create_weather_map(None, map_height)
            st.html(map_html)
        except Exception as e2:
            st.error(f"❌ Fehler beim Laden der Karte: {str(e2)}")

