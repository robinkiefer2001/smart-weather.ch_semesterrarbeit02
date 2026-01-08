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
    temp: {city['temperature'] if isinstance(city['temperature'], (int, float)) else 'null'},
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
    temp: null,
    popup: '{search_popup_escaped}',
    color: '#FF0000',
    type: 'search'
  }}"""
    
    markers_code += "];"
    
    # HTML mit professioneller Leaflet-Karte - swisstopo inspiriert
    leaflet_html = """
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      body, html {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        overflow: hidden;
      }
      #map {
        width: 100%;
        height: MAP_HEIGHT_PX;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        position: relative;
      }
      
      .leaflet-container {
        background: linear-gradient(135deg, #f0f4f8 0%, #e8eef5 100%) !important;
        font-family: inherit;
      }
      
      .leaflet-control-attribution {
        background: rgba(255, 255, 255, 0.85) !important;
        border-radius: 6px;
        padding: 6px 10px !important;
        font-size: 11px;
      }
      
      .leaflet-control-zoom {
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        background: white !important;
      }
      
      .leaflet-control-zoom a {
        color: #2c5aa0 !important;
        font-weight: bold;
        border-radius: 6px;
      }
      
      .leaflet-control-zoom a:hover {
        background: #2c5aa0 !important;
        color: white !important;
      }
      
      .weather-marker-container {
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.18);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        border: 3px solid white;
        position: relative;
      }
      
      .weather-marker-container:hover {
        transform: scale(1.2);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.25);
        filter: brightness(1.1);
      }
      
      .weather-marker-emoji {
        font-size: 24px;
        line-height: 1;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
      }
      
      .weather-marker-temp {
        position: absolute;
        bottom: -18px;
        background: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
        color: #2c5aa0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        white-space: nowrap;
      }
      
      .leaflet-popup-content-wrapper {
        border-radius: 10px;
        background: white !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
        padding: 0 !important;
        border: none !important;
      }
      
      .leaflet-popup-content {
        font-size: 13px;
        padding: 12px 14px !important;
        margin: 0 !important;
        line-height: 1.5;
      }
      
      .leaflet-popup-content strong {
        color: #1a3a52;
        font-size: 14px;
      }
      
      .leaflet-popup-tip {
        background: white !important;
        box-shadow: -2px -2px 4px rgba(0, 0, 0, 0.1);
      }
      
      .leaflet-popup-close-button {
        color: #2c5aa0 !important;
      }
      
      .weather-details {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px;
        font-size: 12px;
        color: #666;
        margin-top: 6px;
        padding-top: 6px;
        border-top: 1px solid #e0e0e0;
      }
      
      .weather-detail-item {
        display: flex;
        align-items: center;
        gap: 4px;
      }
    </style>

    <div id="map"></div>

    <!-- Leaflet & Plugins -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

    <script>
      // Schweiz-Bounds (mit etwas Puffer)
      var swissBounds = L.latLngBounds(
        L.latLng(45.6, 5.6),   // Süd-West
        L.latLng(47.8, 10.5)   // Nord-Ost
      );
      
      // Initialisiere Karte mit Schweiz-Focus
      var map = L.map('map', {
        maxBounds: swissBounds,
        maxBoundsViscosity: 0.8,
        zoomControl: true,
        attributionControl: true,
        center: [46.7, 8.15],
        zoom: 8
      });

      // Hochwertige Basiskarte - Stamen TonerLite (Schweiz-optimiert)
      L.tileLayer(
        'https://tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png',
        {
          maxZoom: 14,
          minZoom: 7,
          attribution: '© swisstopo, © OpenStreetMap contributor',
          className: 'map-base-layer'
        }
      ).addTo(map);

      // Sanfte Schweiz-Grenze
      var swissBox = L.rectangle(swissBounds, {
        color: '#2c5aa0',
        weight: 1.5,
        fillOpacity: 0,
        dashArray: '3, 4',
        lineCap: 'round'
      }).addTo(map);

      // Marker-Daten
      MARKERS_CODE_HERE
      
      // Zeichne alle Marker mit optimiertem Design
      markers.forEach(function(markerData) {
        var isSearch = markerData.type === 'search';
        var markerSize = isSearch ? 50 : 44;
        var fontSize = isSearch ? '28px' : '24px';
        
        // Erstelle Custom Marker mit Temperatur-Badge
        var tempStr = markerData.temp || '--';
        var tempDisplay = typeof tempStr === 'number' ? tempStr.toFixed(1) : tempStr;
        
        var markerHTML = document.createElement('div');
        markerHTML.className = 'weather-marker-container';
        markerHTML.style.width = markerSize + 'px';
        markerHTML.style.height = markerSize + 'px';
        markerHTML.style.background = 'linear-gradient(135deg, ' + markerData.color + ', ' + markerData.color + 'dd)';
        
        var emojiSpan = document.createElement('span');
        emojiSpan.className = 'weather-marker-emoji';
        emojiSpan.style.fontSize = fontSize;
        emojiSpan.textContent = markerData.emoji || '❓';
        markerHTML.appendChild(emojiSpan);
        
        if (tempDisplay !== '--') {
          var tempBadge = document.createElement('div');
          tempBadge.className = 'weather-marker-temp';
          tempBadge.textContent = tempDisplay + '°';
          markerHTML.appendChild(tempBadge);
        }
        
        var customIcon = L.divIcon({
          html: markerHTML.outerHTML,
          iconSize: [markerSize, markerSize + 25],
          iconAnchor: [markerSize/2, markerSize/2],
          popupAnchor: [0, -markerSize/2 - 15],
          className: 'custom-weather-marker'
        });
        
        L.marker([markerData.lat, markerData.lon], {
          icon: customIcon,
          title: markerData.name
        }).bindPopup(markerData.popup, {
          closeButton: true,
          offset: L.point(0, -markerSize/2 - 10),
          maxWidth: 280
        }).on('click', function() {
          this.openPopup();
        }).addTo(map);
      });
      
      // Fit bounds beim Load
      map.fitBounds(swissBounds, {padding: [40, 40]});
      
      // Verhindere Zoom außerhalb der Schweiz
      map.on('zoom', function() {
        if (!map.getBounds().intersects(swissBounds)) {
          map.fitBounds(swissBounds);
        }
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

