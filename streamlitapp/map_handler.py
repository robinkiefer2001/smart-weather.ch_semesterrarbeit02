"""
Kartenfunktionen und Wetter-Overlay für Leaflet
"""
import streamlit as st
import streamlit.components.v1 as components
from api_client import fetch_weather_data
import time


@st.cache_data(ttl=300)
def get_cached_weather_data(lat: float, lon: float) -> dict:
    """Wetterdaten für 5 Minuten cachen um API-Limits zu respektieren."""
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


# 12 strategische Städte für regionale Wetter-Übersicht (bessere API-Performance)
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
    """WMO Wettercodes in visuelle Symbole für schnelle Erfassbarkeit."""
    weather_emojis = {
        0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️", 45: "🌫️", 48: "🌫️",
        51: "🌦️", 53: "🌧️", 55: "🌧️", 61: "🌧️", 63: "🌧️", 65: "🌧️",
        71: "❄️", 73: "❄️", 75: "❄️",
        80: "🌦️", 81: "🌧️", 82: "🌧️",
        95: "⛈️", 99: "⛈️"
    }
    return weather_emojis.get(weather_code, "❓")


def get_weather_color(weather_code: int) -> str:
    """Intuitive Farben für schnelle visuelle Erkennung des Wetters."""
    if weather_code == 0: return "#FFD700"  # Sonne = Gold
    elif weather_code in [1, 2]: return "#87CEEB"  # Wolken = Blau
    elif weather_code in [3]: return "#808080"  # Bedeckt = Grau
    elif weather_code in [45, 48]: return "#A9A9A9"  # Nebel = Dunkelgrau
    elif weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]: return "#4169E1"  # Regen = Königsblau
    elif weather_code in [71, 73, 75]: return "#F0F8FF"  # Schnee = Hellblau
    elif weather_code in [95, 99]: return "#FF6347"  # Gewitter = Rot
    else: return "#808080"


def get_temperature_color(temperature: float) -> str:
    """Temperaturbasierte Farbcodierung wie MeteoSwiss."""
    if isinstance(temperature, str) or temperature is None:
        return "#c0c0c0"  # Grau für keine Daten
    try:
        temp = float(temperature)
        if temp < -20: return "#1e3a8a"  # Dunkles Blau - sehr kalt
        elif temp < -10: return "#3b82f6"  # Kräftiges Blau - kalt
        elif temp < 0: return "#60a5fa"  # Helles Blau - kühl
        elif temp < 5: return "#f5f5f5"  # Weiss - mild
        elif temp < 10: return "#fef3c7"  # Sanftes Hellgelb - warm
        elif temp < 15: return "#fcd34d"  # Helles Gelb - wärmer
        elif temp < 20: return "#fbbf24"  # Kräftiges Gelb - heiss
        else: return "#f59e0b"  # Dunkles Gelb - sehr heiss
    except:
        return "#c0c0c0"


def fetch_city_weather_data() -> list:
    """
    Holt Wetterdaten für alle 12 Städte mit Rate-Limiting.
    Caching verhindert zu häufige API-Calls und respektiert Rate-Limits.
    Bei Fehler werden Fallback-Daten mit "--" verwendet.
    """
    cities_weather = []
    
    for i, city in enumerate(MAJOR_CITIES):
        try:
            # Rate-Limiting: 200ms Verzögerung zwischen API-Anfragen
            if i > 0:
                time.sleep(0.2)
            
            # Versuche Daten aus Cache zu laden (max. 5 Min alt)
            weather_result = get_cached_weather_data(city["lat"], city["lon"])
            
            if weather_result["success"]:
                current_data = weather_result["data"]
                temp_value = current_data.get("temperature_2m", 0)
                weather_code = int(current_data.get("weather_code", 0)) if current_data.get("weather_code") is not None else 0
                
                # Sichere Umwandlung mit Fehlerbehandlung
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
                # Bei Fehler: Standard-Werte zeigen
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
            # Fehler abfangen und mit Dummy-Daten fortfahren
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
    Erstellt eine interaktive Leaflet-Karte mit Wetter-Markern.
    Die Marker zeigen Temperatur und Wetterbedingungen auf der Swisstopo-Basiskarte.
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
        # Nutze temperaturbasierte Farbe statt Wetterkode
        color = get_temperature_color(city["temperature"])
        temp_str = str(city["temperature"]) if city["temperature"] != "--" else "--"
        emoji = city["weather_emoji"]
        
        # Escape HTML-Zeichen für JavaScript
        cloud_str = str(city['cloud_cover']) if city['cloud_cover'] != "--" else "--"
        humidity_str = str(city['humidity']) if city['humidity'] != "--" else "--"
        wind_str = str(city['wind_speed']) if city['wind_speed'] != "--" else "--"
        
        popup_html = f"""<div style="text-align: center; font-family: Arial, sans-serif; padding: 10px;">
<strong>{city['name']}</strong><br>
<div style="font-size: 32px;">{emoji}</div>
<strong style="color: #FF6B6B; font-size: 20px;">{temp_str}°C</strong><br>
<small>☁️ {cloud_str}% | 💧 {humidity_str}% | 💨 {wind_str} km/h</small>
</div>"""
        
        # Escape für JavaScript - besonders wichtig für Prozentzeichen
        popup_escaped = popup_html.replace("'", "\\'").replace("\n", " ").replace("%", "%%")
        
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
      
      // Initialisiere Karte mit Schweiz-Focus (bessere Skalierung)
      var map = L.map('map', {
        maxBounds: swissBounds,
        maxBoundsViscosity: 0.8,
        zoomControl: true,
        attributionControl: true,
        center: [46.8, 8.2],
        zoom: 9
      });

      // Test mit OpenStreetMap (funktioniert zuverlässig)
      var swisstopoLayer = L.tileLayer(
        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        {
          maxZoom: 19,
          minZoom: 7,
          attribution: '&copy; OpenStreetMap contributors',
          crossOrigin: true,
          className: 'map-tiles'
        }
      ).addTo(map);

      // Dunkler Hintergrund für besseren Kontrast
      map.getPane('mapPane').style.filter = 'brightness(0.95) saturate(1.1)';

      // Swiss Meteo Radar Overlay - Live Niederschlagsdaten
      var radarLayer = L.tileLayer(
        'https://tile.maps.verwalt.ch/radar/{z}/{x}/{y}.png',
        {
          opacity: 0.5,
          attribution: '© MeteoSwiss',
          maxZoom: 15,
          minZoom: 7,
          crossOrigin: 'anonymous'
        }
      ).addTo(map);

      // Layer-Control für Benutzer zum An-/Ausschalten
      var baseMaps = {
        'Landeskarte': swisstopoLayer
      };
      
      var overlayMaps = {
        'Radar (Live)': radarLayer
      };
      
      L.control.layers(baseMaps, overlayMaps, {
        position: 'topright',
        collapsed: true
      }).addTo(map);

      // Marker-Daten
      MARKERS_CODE_HERE
      
      // Zeichne alle Marker mit optimiertem Design
      markers.forEach(function(markerData) {
        var isSearch = markerData.type === 'search';
        var markerSize = isSearch ? 60 : 50;  // Grössere Marker
        var fontSize = isSearch ? '32px' : '28px';
        
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
      
      // Verhindere Zoom ausserhalb der Schweiz
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
    Rendet die interaktive Wetterkarte im Streamlit-Frontend.
    Mit Fehlerbehandlung und Fallback-Darstellung.
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
        # Fallback: Zeige Karte ohne Wetterdaten wenn API fehlschlägt
        st.warning(f"⚠️ Konnte Wetterdaten nicht laden: {str(e)}")
        st.info("Die Karte wird mit Standarddaten angezeigt...")
        
        try:
            map_html = create_weather_map(None, search_location=None, map_height=map_height)
            components.html(map_html, height=map_height)
        except Exception as e2:
            st.error(f"❌ Fehler beim Laden der Karte: {str(e2)}")

