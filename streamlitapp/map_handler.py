"""
Kartenfunktionen und Wetter-Overlay für Leaflet
"""
import streamlit as st
import streamlit.components.v1 as components
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
                weather_code = int(current_data.get("weather_code", 0)) if current_data.get("weather_code") is not None else 0
                
                # Sichere Umwandlung der Werte
                try:
                    cloud_cover = round(float(current_data.get("cloud_cover") or 0), 0)
                except (ValueError, TypeError):
                    cloud_cover = 0
                    
                try:
                    wind_speed = round(float(current_data.get("wind_speed_10m") or 0), 1)
                except (ValueError, TypeError):
                    wind_speed = 0
                    
                try:
                    humidity = round(float(current_data.get("relative_humidity_2m") or 0), 0)
                except (ValueError, TypeError):
                    humidity = 0
                
                cities_weather.append({
                    "name": city["name"],
                    "lat": city["lat"],
                    "lon": city["lon"],
                    "temperature": round(float(temp_value), 1) if temp_value else 0,
                    "weather_code": weather_code,
                    "weather_emoji": get_weather_emoji(weather_code),
                    "cloud_cover": int(cloud_cover),
                    "wind_speed": wind_speed,
                    "humidity": int(humidity),
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
    emoji: '{emoji}',
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
    emoji: '📍',
    popup: '{search_popup_escaped}',
    color: '#FF0000',
    type: 'search'
  }}"""
    
    markers_code += "];"
    
    # HTML mit Leaflet-Karte - Professionelles Design
    leaflet_html = """
    <style>
      body, html {
        margin: 0;
        padding: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      }
      #map {
        width: 100%;
        height: MAP_HEIGHT_PX;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        overflow: hidden;
      }
      .leaflet-container {
        background-color: #e8f1f8 !important;
      }
      .weather-marker {
        font-weight: bold;
        text-align: center;
        border-radius: 50%;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        cursor: pointer;
        backdrop-filter: blur(4px);
      }
      .weather-marker:hover {
        transform: scale(1.15);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
      }
      .leaflet-popup-content {
        font-family: 'Segoe UI', sans-serif;
        margin: 0;
      }
      .leaflet-popup-content-wrapper {
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.98);
        padding: 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
      }
      .leaflet-popup-tip {
        background: rgba(255, 255, 255, 0.98);
      }
    </style>

    <div id="map"></div>

    <!-- Leaflet CSS & JS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://unpkg.com/leaflet-heat@0.2.0/dist/leaflet-heat.js"></script>

    <script>
      // Bounds für Schweiz-Ausschnitt
      var bounds = L.latLngBounds(
        L.latLng(45.3, 5.8),   // Süd-West
        L.latLng(47.9, 10.6)   // Nord-Ost
      );

      // Karte mit professionellem Styling
      var map = L.map('map', {
        maxBounds: bounds,
        maxBoundsViscosity: 1.0,
        zoomControl: true,
        attributionControl: false
      }).fitBounds(bounds);

      // Basiskarte mit hochwertigerem Tile-Layer
      L.tileLayer(
        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        {
          maxZoom: 14,
          minZoom: 6,
          opacity: 0.85,
          className: 'map-tiles'
        }
      ).addTo(map);

      // Sanfte Rahmen um die Schweiz
      L.rectangle(bounds, {
        color: "#2c5aa0",
        weight: 2,
        fillOpacity: 0,
        dashArray: "5, 5"
      }).addTo(map);

      // Marker-Daten
      MARKERS_CODE_HERE
      
      // Marker hinzufügen mit modernem Design
      markers.forEach(function(markerData) {
        var isSearch = markerData.type === 'search';
        var markerSize = isSearch ? 45 : 38;
        var opacity = isSearch ? 0.95 : 0.90;
        var borderWeight = isSearch ? 4 : 2;
        var borderColor = isSearch ? '#fff' : '#fff';
        
        // Erstelle SVG-basiertes Icon für besseres Rendering
        var customIcon = L.divIcon({
          html: `<div style="
            width: ${markerSize}px;
            height: ${markerSize}px;
            border-radius: 50%;
            background: linear-gradient(135deg, ${markerData.color} 0%, ${markerData.color}dd 100%);
            border: ${borderWeight}px solid ${borderColor};
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: ${isSearch ? '24px' : '20px'};
            font-weight: bold;
            color: white;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
            backdrop-filter: blur(4px);
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            cursor: pointer;
          " class="weather-marker">
            <span>${markerData.emoji || '❓'}</span>
          </div>`,
          iconSize: [markerSize, markerSize],
          className: 'custom-marker'
        });
        
        var marker = L.marker([markerData.lat, markerData.lon], {
          icon: customIcon,
          title: markerData.name
        }).bindPopup(markerData.popup, {
          className: 'custom-popup',
          closeButton: true,
          offset: [0, -markerSize/2 - 10]
        }).addTo(map);
        
        // Hover-Effekt
        marker.on('mouseover', function() {
          this.openPopup();
        });
      });
    </script>
    """
    
    # Ersetze Platzhalter mit echten Werten
    leaflet_html = leaflet_html.replace("MAP_HEIGHT_PX", f"{map_height}px")
    leaflet_html = leaflet_html.replace("MARKERS_CODE_HERE", markers_code)
    
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
        map_html = create_weather_map(cities_weather, search_location=None, map_height=map_height)
        components.html(map_html, height=map_height)
        
    except Exception as e:
        # Fallback: Zeige Standard-Karte ohne Daten
        st.warning(f"⚠️ Konnte Wetterdaten nicht laden: {str(e)}")
        st.info("Die Karte wird mit Standarddaten angezeigt...")
        
        try:
            map_html = create_weather_map(None, search_location=None, map_height=map_height)
            components.html(map_html, height=map_height)
        except Exception as e2:
            st.error(f"❌ Fehler beim Laden der Karte: {str(e2)}")

