import streamlit as st

st.set_page_config(
    page_title="Datenschutz - Smart Weather Switzerland",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🔒 Datenschutz")

st.markdown("""
## Datenschutzerklärung

### 1. Verantwortliche Person
**Robin Kiefer**
Schulprojekt für Wettervorhersage

---

### 2. Allgemeine Informationen zur Datenschutz

Diese Webseite ist ein Schulprojekt und sammelt **keine persönlichen Daten** von Besuchern.

---

### 3. Was wir NICHT sammeln

- ❌ Keine IP-Adressen
- ❌ Keine Cookies
- ❌ Keine Nutzer-IDs
- ❌ Keine Standortdaten von Geräten
- ❌ Keine Browserdaten
- ❌ Keine Suchverlauf
- ❌ Keine E-Mail-Adressen

---

### 4. Verwendete externe Dienste

#### Open-Meteo API
- **Zweck**: Wetterdaten abrufen
- **Datenschutz**: [open-meteo.com/en/privacy](https://open-meteo.com/en/privacy)
- **Datenübertragung**: Nur geografische Koordinaten (Breitengrad/Längengrad)

#### OpenStreetMap & Leaflet
- **Zweck**: Kartendarstellung
- **Datenschutz**: [openstreetmap.org/copyright](https://www.openstreetmap.org/copyright)
- **Datenübertragung**: Nur sichtbare Kartenausschnitte

#### Swiss Meteo Radar
- **Zweck**: Wetter-Radarschichten
- **Datenübertragung**: Anonyme Abfragen

---

### 5. Lokale Datenspeicherung

Die Anwendung speichert **lokal auf Ihrem Gerät**:
- 📍 Zuletzt gesuchte Orte (temporär)
- 🌡️ Angezeigte Wetterdaten (temporär)

Diese Daten werden:
- Nicht auf Server übertragen
- Nicht dauerhaft gespeichert
- Bei Schliessen der Seite gelöscht

---

### 6. Ihre Rechte

Da wir keine persönlichen Daten sammeln, gelten die Datenschutzrechte eingeschränkt. Bei Fragen kontaktieren Sie bitte direkt die verantwortliche Person.

---

### 7. Änderungen dieser Datenschutzerklärung

Wir behalten uns das Recht vor, diese Datenschutzerklärung jederzeit zu aktualisieren. Die aktuelle Version ist immer auf dieser Seite verfügbar.

---

*Letzte Aktualisierung: Januar 2026*
""")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 12px;">
    <a href="/" style="color: #3b82f6; text-decoration: none;">← Zurück zur Wetterkarte</a>
</div>
""", unsafe_allow_html=True)
