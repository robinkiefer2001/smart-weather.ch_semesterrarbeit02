#!/usr/bin/env python3
"""
Test-Skript zur Überprüfung der Kartenfunktion
"""

import streamlit as st
import streamlit.components.v1 as components

st.title("Test Wetter-Karte")

# Einfache HTML Karte zum Testen
map_html = """
<div id="map" style="width: 100%; height: 600px; position: relative;"></div>

<!-- Leaflet CSS & JS -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<script>
    // Bounds für Schweiz
    var bounds = L.latLngBounds(
        L.latLng(45.5, 5.5),
        L.latLng(48.0, 11.0)
    );
    
    // Karte initialisieren
    var map = L.map('map', {
        maxBounds: bounds,
        maxBoundsViscosity: 1.0
    }).fitBounds(bounds);
    
    // OpenStreetMap Layer
    L.tileLayer(
        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        {
            maxZoom: 14,
            minZoom: 6,
            attribution: '© OpenStreetMap contributors'
        }
    ).addTo(map);
    
    // Test-Marker
    var cities = [
        {name: "Zürich", lat: 47.3769, lon: 8.5472},
        {name: "Bern", lat: 46.9479, lon: 7.4474},
        {name: "Genf", lat: 46.2044, lon: 6.1432},
    ];
    
    cities.forEach(function(city) {
        L.circleMarker([city.lat, city.lon], {
            radius: 25,
            fillColor: '#FFD700',
            color: '#333',
            weight: 2,
            opacity: 0.9,
            fillOpacity: 0.85
        }).bindPopup('<div style="text-align: center;"><b>' + city.name + '</b><br>Test Marker</div>').addTo(map);
    });
    
    // Rahmen-Rechteck
    L.rectangle(bounds, {
        color: "#00aaff",
        weight: 2,
        fillOpacity: 0.0
    }).addTo(map);
</script>
"""

st.write("Hier sollte eine Karte mit 3 Test-Markern sichtbar sein:")
components.html(map_html, height=650, scrolling=False)

st.success("✅ Wenn die Karte sichtbar ist, funktioniert die Leaflet-Integration!")
