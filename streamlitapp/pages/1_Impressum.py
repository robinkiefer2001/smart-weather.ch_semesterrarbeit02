import streamlit as st

st.set_page_config(
    page_title="Impressum - Smart Weather Switzerland",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("📋 Impressum")

st.markdown("""
## Angaben gemäss Impressumspflicht

### Betreiber
**Smart Weather Switzerland**
Schulprojekt für Wettervorhersage

### Verantwortliche Person
**Robin Kiefer**

### Zweck
Diese Webseite ist ein Schulprojekt und dient ausschliesslich zu Bildungszwecken.

---

## Haftungsausschluss

### Inhalt der Webseite
Die Informationen auf dieser Webseite werden mit grösstmöglicher Sorgfalt erstellt. Wir übernehmen jedoch keine Gewähr für die Richtigkeit, Vollständigkeit oder Aktualität der bereitgestellten Informationen. Insbesondere können Wettervorhersagen ungenau oder fehlerhaft sein.

### Externe Links
Diese Webseite enthält Links zu externen Webseiten von Dritten. Für den Inhalt dieser externen Webseiten sind die jeweiligen Betreiber verantwortlich. Wir übernehmen keine Haftung für fremde Inhalte.

### Datenquellen
- **Wetterdaten**: Open-Meteo API
- **Kartendaten**: OpenStreetMap & Swiss Meteo Radar
- **Standortdaten**: Lokale Datenbank

---

## Technische Informationen

**Entwickelt mit:**
- Python & Streamlit
- Open-Meteo API
- Leaflet Kartenbibliothek

**Kein Tracking oder Datensammlung** - Diese Seite speichert keine persönlichen Daten.

---

*Letzte Aktualisierung: Januar 2026*
""")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 12px;">
    <a href="/" style="color: #3b82f6; text-decoration: none;">← Zurück zur Wetterkarte</a>
</div>
""", unsafe_allow_html=True)
