import streamlit as st

st.set_page_config(
    page_title="Impressum - Smart Weather Switzerland",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Impressum")

st.markdown("""
## Angaben gemäss Impressumspflicht

### 1. Betreiber und Verantwortliche Person

**Smart Weather Switzerland** ist ein Schulprojekt für Echtzeit-Wettervorhersage in der Schweiz.

**Verantwortliche Person:**
- Name: Robin Kiefer
- Funktion: Projektverantwortlicher
- Schule: [Schulname einfügen]
- Zweck: Schulprojekt im Rahmen der Semesterarbeit

---

### 2. Projektbeschreibung

**Smart Weather Switzerland** ist eine interaktive Webapplikation, die:
- Echtzeit-Wetterdaten für Schweizer Städte und Orte anzeigt
- Stündliche Vorhersagen mit detaillierten Diagrammen bereitstellt
- 14-Tages-Prognosen mit Wetterverlauf darstellt
- Eine interaktive Karte mit Wetter-Radarüberlagerung bietet
- Lokale Wetterdaten durchsuchbar macht

Das Projekt dient **ausschliesslich zu Bildungszwecken** und ist kostenlos verfügbar.

---

### 3. Haftungsausschluss

#### 3.1 Inhalt der Webseite
Die Informationen auf dieser Webseite werden mit grösstmöglicher Sorgfalt erstellt und basieren auf verfügbaren Wetterdaten der Open-Meteo API. Wir übernehmen jedoch **keine Gewähr** für:
- Richtigkeit und Vollständigkeit der bereitgestellten Informationen
- Aktualität und Genauigkeit von Wettervorhersagen
- Fehlerfehler oder technische Störungen
- Verfügbarkeit des Dienstes zu jeder Zeit

**Wettervorhersagen sind Prognosen und keine Garantien.** Extreme Wetterereignisse können unerwartet auftreten.

#### 3.2 Externe Dienste und Links
Diese Webseite nutzt externe Dienste und kann Links zu externen Webseiten enthalten:
- **Open-Meteo API**: Wetterdaten und Prognosen
- **OpenStreetMap**: Kartendaten und -darstellung
- **Leaflet**: Kartenbibliothek für Kartenvisualisierung
- **Swiss Meteo Radar**: Radarbilder für Niederschlagsvorhersagen

Für den Inhalt dieser externen Services und Links sind die jeweiligen Betreiber verantwortlich. Wir haben keinen Einfluss auf deren Inhalte und übernehmen keine Haftung für fremde Inhalte.

#### 3.3 Verfügbarkeit und Störungshaftung
Der Dienst wird kostenlos angeboten und "AS IS" (wie vorhanden) bereitgestellt. Wir können keine Garantie für ununterbrochene Verfügbarkeit geben. Wartungsarbeiten und Ausfallzeiten sind möglich.

---

### 4. Datenquellen

| Service | Quelle | Zweck | Link |
|---------|--------|-------|------|
| **Wetterdaten** | Open-Meteo API | Stündliche und tägliche Vorhersagen | [open-meteo.com](https://open-meteo.com) |
| **Kartendaten** | OpenStreetMap | Grundkarte und Ortssuche | [openstreetmap.org](https://openstreetmap.org) |
| **Radarbilder** | MeteoSchweiz | Wetter-Radarüberlagerung | [meteo.admin.ch](https://www.meteo.admin.ch) |
| **Kartenvisualisierung** | Leaflet | Interaktive Kartendarstellung | [leafletjs.com](https://leafletjs.com) |

---

### 5. Technische Informationen

**Entwickelt mit:**
- **Backend**: Python 3.x
- **Frontend Framework**: Streamlit
- **Kartenbibliothek**: Leaflet.js
- **API-Kommunikation**: HTTP/REST

**Keine Cookie-Speicherung** – Diese Seite verwendet keine Tracking-Cookies oder Überwachungstechnologien.

---

### 6. Verwendete Technologien und Lizenzen

- **Streamlit**: Open Source, BSD License
- **Leaflet**: Open Source, BSD 2-Clause License
- **Python**: Open Source, Python Software Foundation License

---

### 7. Kontakt und Feedback

**Bei Fragen, Problemen oder Feedback:**
- Verantwortliche Person: Robin Kiefer
- Projekttyp: Schulprojekt/Semesterarbeit
- Art der Anfrage: Schulprojekt

---

### 8. Rechtliche Hinweise

Diese Webseite wird bereitgestellt "wie vorhanden" ohne jegliche ausdrückliche oder implizierte Garantien. Der Betreiber übernimmt keine Haftung für:
- Direkte oder indirekte Schäden
- Datenverluste oder Fehler
- Folgeschäden aus der Nutzung oder dem Nichtfunktionieren dieser Webseite

**Diese Bedingungen unterliegen den Gesetzen der Schweiz.**

---

*Letzte Aktualisierung: Januar 2026*
*Version: 1.0*
""")

st.markdown("---")

st.markdown("""
<div style="text-align: center; color: gray; font-size: 12px; margin-top: 20px;">
    <p>Navigation: Wählen Sie eine Seite in der linken Sidebar oder kehren Sie zur Wetterkarte zurück</p>
</div>
""", unsafe_allow_html=True)

---

*Letzte Aktualisierung: Januar 2026*
""")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 12px;">
    <a href="/" style="color: #3b82f6; text-decoration: none;">← Zurück zur Wetterkarte</a>
</div>
""", unsafe_allow_html=True)
