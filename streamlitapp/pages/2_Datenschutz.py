import streamlit as st

st.set_page_config(
    page_title="Datenschutz - Smart Weather Switzerland",
    page_icon="🔒",
    layout="wide"
)

st.title("🔒 Datenschutzerklärung")

st.markdown("""
## Datenschutzerklärung für Smart Weather Switzerland

### 1. Verantwortliche Person und Kontakt

**Verantwortliche Person für Datenschutz:**
- Name: Robin Kiefer
- Funktion: Projektleiter
- Projekttyp: Schulprojekt / Semesterarbeit
- Zweck: Bildungszwecke

**Hinweis:** Dieses Projekt ist ein Schulprojekt ohne kommerzielle Absicht. Es unterliegt den geltenden Datenschutzbestimmungen der Schweiz.

---

### 2. Allgemeine Datenschutzpolitik

**Kernprinzip:** Diese Webseite sammelt **KEINE persönlichen Daten** von Besuchern.

Das Projekt wurde mit **Datenschutz-by-Design** entwickelt:
- ✅ Keine Registrierung erforderlich
- ✅ Keine Benutzerkonten
- ✅ Keine Datensammlung
- ✅ Keine Überwachung

---

### 3. Was wir NICHT sammeln und speichern

Wir sammeln **aktiv NICHT**:

| Datentyp | Status |
|----------|--------|
| IP-Adressen | ❌ Nicht gesammelt |
| Browser-Cookies | ❌ Nicht gesetzt |
| Nutzer-IDs / Session-IDs | ❌ Nicht erstellt |
| Gerätestandort | ❌ Nicht abgefragt |
| Browserdaten/User-Agent | ❌ Nicht erfasst |
| Suchverlauf | ❌ Nicht protokolliert |
| E-Mail-Adressen | ❌ Nicht gesammelt |
| Telefonnummern | ❌ Nicht gesammelt |
| Namen oder persönliche Daten | ❌ Nicht erfasst |
| Klickverhalten / Analytics | ❌ Nicht verfolgt |
| Nutzerprofile | ❌ Nicht erstellt |

---

### 4. Verwendete externe Services und deren Datenschutz

Diese Anwendung nutzt folgende externe Services. Hier finden Sie Informationen zu deren Datenschutzpraktiken:

#### 4.1 Open-Meteo API
- **Zweck**: Abruf von Wetterdaten und Prognosen
- **Datenübertragung**: Nur geografische Koordinaten (Breitengrad/Längengrad)
- **Speicherung**: Open-Meteo speichert Anfrageinformationen ggf. für Analysezwecke
- **Datenschutzrichtlinie**: [open-meteo.com/en/privacy](https://open-meteo.com/en/privacy)
- **GDPR-Konformität**: Ja
- **Hinweis**: Das Projekt speichert keine API-Anfragen lokal

#### 4.2 OpenStreetMap (OSM)
- **Zweck**: Kartendaten und Darstellung von Geographiedaten
- **Datenübertragung**: Kartenausschnitt-Koordinaten für Kartentiles
- **Speicherung**: OSM kann Anfragemuster für Statistiken erfassen
- **Datenschutzrichtlinie**: [openstreetmap.org/copyright](https://www.openstreetmap.org/copyright)
- **GDPR-Konformität**: Ja (Community-betrieben, kein Tracking)

#### 4.3 Leaflet.js
- **Zweck**: JavaScript-Bibliothek für Kartenvisualisierung
- **Datenübertragung**: Keine direkten Datenübertragungen
- **Speicherung**: Lokal im Browser
- **Lizenz**: BSD 2-Clause Open Source
- **Datenschutz**: Keine Datensammlung durch Leaflet

#### 4.4 Streamlit (Hosting-Framework)
- **Zweck**: Webapplikation-Framework
- **Datenübertragung**: Abhängig von Deployment-Konfiguration
- **Speicherung**: Abhängig vom Server (wenn auf Streamlit Cloud gehostet)
- **Datenschutzrichtlinie**: [streamlit.io/privacy](https://streamlit.io/privacy)

#### 4.5 MeteoSchweiz Radarbilder
- **Zweck**: Wetter-Radardarstellung
- **Datenübertragung**: Radarbildabfragen (keine Personendaten)
- **Speicherung**: Keine Speicherung auf unserem Server
- **Datenschutz**: [meteo.admin.ch](https://www.meteo.admin.ch)

---

### 5. Lokale Datenspeicherung (Browser-seitig)

Die Anwendung speichert **temporär auf Ihrem lokalen Gerät**:

**Was wird gespeichert:**
- 📍 Zuletzt gesuchte Orte (im Browser Session Storage)
- 🌡️ Angezeigte Wetterdaten (im RAM während der Session)
- 🗺️ Kartenzoom-Level und -Position (Streamlit Session State)

**Wichtig:**
- ✅ Diese Daten werden **NICHT auf Server übertragen**
- ✅ Sie werden **NICHT dauerhaft gespeichert**
- ✅ Sie werden **beim Schliessen des Browsers gelöscht**
- ✅ Sie befinden sich in **Ihrem lokalen Speicher**

---

### 6. Cookies und Tracking

**Cookies:** ❌ Diese Seite setzt **keine Cookies**.

**Tracking-Technologien:**
- ❌ Keine Google Analytics
- ❌ Keine Facebook Pixel
- ❌ Keine Hotjar oder ähnliche Session-Recording-Tools
- ❌ Keine Werbenetze oder Tracking-Pixel
- ❌ Keine Retargeting-Codes

---

### 7. Ihre Rechte bezüglich Datenschutz

Da wir keine persönlichen Daten sammeln, sind klassische Datenschutzrechte (DSGVO Artikel 15-22) teilweise nicht anwendbar. Jedoch haben Sie das Recht:

- **Auskunftsrecht**: Sie können anfragen, welche Daten wir über Sie haben (Antwort: keine)
- **Recht auf Löschung**: Nicht anwendbar (da keine Daten gespeichert)
- **Recht auf Berichtigung**: Nicht anwendbar (da keine Daten gespeichert)
- **Recht auf Datenportabilität**: Nicht anwendbar (da keine Daten gespeichert)

**Bei Fragen zu Ihren Rechten:**
Kontaktieren Sie bitte direkt die verantwortliche Person: Robin Kiefer

---

### 8. Sicherheit

**Datensicherheit auf Anwendungsebene:**
- Keine Speicherung von Benutzerdaten auf Servern
- Keine Datenbanken mit persönlichen Informationen
- HTTPS-Verschlüsselung (wenn bereitgestellt)
- Minimale externe API-Abhängigkeiten

**Externe Service-Sicherheit:**
- Open-Meteo: SSL/TLS-verschlüsselt
- OpenStreetMap: SSL/TLS-verschlüsselt
- Streamlit: Abhängig vom Hosting-Provider

---

### 9. Änderungen dieser Datenschutzerklärung

Wir behalten uns das Recht vor, diese Datenschutzerklärung jederzeit zu aktualisieren, um:
- Neue Features oder Services zu dokumentieren
- Änderungen in externen Services zu berücksichtigen
- Gesetzliche Anforderungen zu erfüllen

**Benachrichtigung:** Wichtige Änderungen werden auf dieser Seite angekündigt.

---

### 10. Kontakt und Fragen zum Datenschutz

**Bei Fragen zu dieser Datenschutzerklärung oder zum Datenschutz allgemein:**

- Verantwortliche Person: Robin Kiefer
- Projekttyp: Schulprojekt
- Art der Anfrage: Bitte geben Sie an, ob Sie Fragen zum Datenschutz, technische Fragen oder Feedback haben

---

### 11. Rechtliche Grundlagen

Diese Datenschutzerklärung basiert auf:
- **Bundesgesetz über den Datenschutz (DSG)** - Schweiz
- **DSGVO** - Europäische Union (für EU-Zugriffe)
- **Industrielle Best Practices** für Webapplikationen

---

### 12. Zusammenfassung

| Punkt | Antwort |
|-------|--------|
| **Sammeln wir Daten?** | ❌ Nein |
| **Speichern wir Daten?** | ❌ Nein |
| **Geben wir Daten an Dritte?** | ❌ Nein |
| **Nutzen wir Cookies?** | ❌ Nein |
| **Nutzen wir Tracking?** | ❌ Nein |
| **Ist die App GDPR-konform?** | ✅ Ja |
| **Ist die App sicher?** | ✅ Ja (keine Datenspeicherung) |

---

*Letzte Aktualisierung: Januar 2026*  
*Version: 1.0*  
*Status: Schulprojekt*
""")

st.markdown("---")
st.markdown("Navigation: Nutzen Sie die Sidebar oder die Links auf der Startseite")
