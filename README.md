# SmartWeather.ch – Projekt Repository

Dieses Repository enthält die Semesterarbeit **SmartWeather.ch** – eine webbasierte Wetter-Applikation für Schweizer Standorte, entwickelt nach agilen Projektmanagement-Prinzipien.

---

## Dokumentation

### Zentrale Projekt-Dokumente

| Dokument | Beschreibung | Zielgruppe |
|----------|--------------|------------|
| **[Project Overview](./docs/PROJECT_OVERVIEW.md)** | Umfassende Projektübersicht mit Vision, Zielen, Architektur, Technologie-Stack und Roadmap. **Start hier für einen Gesamtüberblick.** | Alle Stakeholder, Erstbesucher |
| **[Projectworkbook](./docs/projectworkbook.md)** | Detaillierte Sprint-Dokumentation mit User Stories, Tasks, Deliverables, Reviews, Retrospektiven und technischen Worklogs. **Für agiles Projektmanagement und Entwicklungsdetails.** | Projektleiter, Entwickler, Bewerter |

### Was ist der Unterschied?

- **PROJECT_OVERVIEW.md** = "Was ist das Projekt?" – Vision, Gesamtarchitektur, langfristige Planung
- **projectworkbook.md** = "Wie wurde entwickelt?" – Sprint-für-Sprint Dokumentation, operative Details, technische Implementierung

---

## Quick Start

### Für Neue im Projekt

1. **Lies zuerst:** [Project Overview](./docs/PROJECT_OVERVIEW.md) – verstehe Vision und Architektur
2. **Dann:** [Projectworkbook](./docs/projectworkbook.md) – verstehe die Entwicklung Sprint für Sprint
3. **Code ansehen:** `streamlitapp/app.py` – die Hauptanwendung

### Lokales Setup (Entwicklung)

```bash
# Repository klonen
git clone https://gitlab.com/hf9064413/smart-weather.ch_semesterrarbeit02.git
cd smart-weather.ch_semesterrarbeit02

# Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies installieren
pip install -r requirements_streamlit.txt

# Datenbank-Verbindung konfigurieren
# (secrets.toml erstellen - siehe Projektdokumentation)

# App starten
streamlit run streamlitapp/app.py
```

### Live-Version

Die produktive Anwendung ist erreichbar unter: **https://smart-weather.ch**

---

## Repository-Struktur

```
smart-weather.ch_semesterrarbeit02/
├── docs/
│   ├── PROJECT_OVERVIEW.md        # Projektübersicht & Architektur
│   └── projectworkbook.md         # Sprint-Dokumentation & Worklogs
├── streamlitapp/
│   └── app.py                     # Haupt-Applikation (Streamlit)
├── scripts/
│   ├── get-locations.py           # Import Schweizer Ortsdaten
│   └── locaction_cantons.csv      # CSV mit Orten & Kantonen
├── get-weatherdata.py             # API-Abfrage Script
├── insert_weather_data.py         # Datenbank-Insert Script
├── requirements.txt               # Python Dependencies (Backend)
├── requirements_streamlit.txt     # Python Dependencies (Streamlit)
└── README.md                      # Diese Datei
```

---

## Technologie-Stack

- **Frontend:** Streamlit, Pandas, streamlit-calendar
- **Backend:** Python 3.12, PostgreSQL 16, Open-Meteo API
- **Infrastruktur:** Ubuntu 22.04 LTS (Hetzner), systemd, HTTPS (Loadbalancer)
- **Tools:** Git, Jira, pgAdmin

Detaillierte Informationen: [Technology Stack in PROJECT_OVERVIEW.md](./docs/PROJECT_OVERVIEW.md#technologie-stack)

---

## Projekt-Status

| Sprint | Status | Highlights |
|--------|--------|------------|
| Sprint 0 | Abgeschlossen | Repository, Jira, Hetzner Account, Basis-Dokumentation |
| Sprint 1 | Abgeschlossen | Server-Setup, Domain, HTTPS, PostgreSQL, Firewall |
| Sprint 2 | Abgeschlossen | systemd-Service, Git-Integration, Wetterdaten-Visualisierung, Direkte API-Integration |
| Sprint 3 | Abgeschlossen | Code-Refactoring (modulare Struktur), UI-Verbesserungen, erweiterte Standortsuche |

**Aktuelle Version:** Sprint 3 (Januar 2026)  
**Story Points Sprint 3:** 16

---

## Features

### Kernfunktionalitäten

**Standortsuche**
- Suche nach Schweizer Orten
- Unterstützung für Kantone und Postleitzahlen
- Dropdown-Auswahl bei mehreren Treffern

**Wetterdaten-Visualisierung**
- Aktuelle Wetterbedingungen (Temperatur, Windgeschwindigkeit, Niederschlag)
- Stündliche Vorhersagen mit interaktiven Charts
- 7-Tage-Wettervorhersage
- 10+ verschiedene Wetter-Metriken (UV-Index, Luftfeuchtigkeit, Wolkenbedeckung, etc.)

**Interaktive Charts**
- Temperatur-Verlauf (gefühlt & tatsächlich)
- Niederschlag & Schneefall
- Windgeschwindigkeit & Böen
- Luftdruck & Luftfeuchtigkeit
- UV-Index & Wolkenbedeckung
- Und mehr...

**Benutzerfreundliches UI**
- Modulare Code-Architektur (4 separate Module)
- Responsive Design
- Deutsche Lokalisierung
- Wettersymbole und Icons
- Kalenderansicht für Tagesauswahl

**Technische Highlights**
- Direkte API-Integration (Open-Meteo)
- PostgreSQL-Datenbank mit Geodaten
- Automatischer systemd-Service
- Git-Integration für Auto-Updates
- HTTPS-Verschlüsselung

---

## Architektur

### System-Komponenten

```
┌─────────────────┐
│   Benutzer      │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────────────────┐
│  Hetzner Loadbalancer       │
│  (SSL-Termination)          │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Ubuntu Server              │
│  ├─ Streamlit App           │
│  │  (systemd-Service)       │
│  └─ PostgreSQL DB           │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Open-Meteo API             │
│  (Wetterdaten)              │
└─────────────────────────────┘
```

### Code-Struktur (Sprint 3)

Die Applikation ist in modulare Komponenten aufgeteilt:

- **`api_client.py`** – API-Kommunikation mit Open-Meteo
- **`database.py`** – PostgreSQL-Verbindung und Queries
- **`data_handlers.py`** – Datenverarbeitung mit Pandas
- **`ui_components.py`** – UI-Komponenten und Charts
- **`app.py`** – Hauptanwendung und Orchestrierung

---

## Development

### Voraussetzungen

- Python 3.12+
- PostgreSQL 16+
- Git
- Virtual Environment

### Installation & Setup

```bash
# 1. Repository klonen
git clone https://gitlab.com/hf9064413/smart-weather.ch_semesterrarbeit02.git
cd smart-weather.ch_semesterrarbeit02

# 2. Virtual Environment erstellen und aktivieren
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Dependencies installieren
pip install -r requirements_streamlit.txt

# 4. Datenbank konfigurieren
# Erstelle .streamlit/secrets.toml mit DB-Credentials:
# [connections.postgresql]
# host = "your-db-host"
# port = 5432
# database = "your-database"
# username = "your-username"
# password = "your-password"

# 5. Schweizer Ortsdaten importieren (optional)
python scripts/get-locations.py

# 6. App starten
streamlit run streamlitapp/app.py
```

Die App läuft dann unter `http://localhost:8501`

### Datenbank-Schema

```sql
-- Geodaten für Schweizer Orte
CREATE TABLE geo_location (
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    name VARCHAR(100),
    country_code VARCHAR(2),
    canton VARCHAR(2),
    PRIMARY KEY (latitude, longitude)
);

-- Weitere Tabellen: weather_current, weather_hourly, weather_daily
-- Details siehe projectworkbook.md
```

---

## Deployment

Die Applikation läuft als systemd-Service auf einem Ubuntu-Server:

```bash
# Service Status prüfen
sudo systemctl status streamlit

# Service neustarten
sudo systemctl restart streamlit

# Logs anzeigen
sudo journalctl -u streamlit -f
```

Das Deployment-Script (`run_smartweather.sh`) führt automatisch ein Git-Pull durch und startet die Applikation.

---

## API-Datenquellen

**Open-Meteo API**
- Kostenlose Wetter-API ohne API-Key
- Dokumentation: https://open-meteo.com
- Daten: Aktuelle Wetterdaten, stündliche & tägliche Vorhersagen

**Geocoding API**
- Für Standortsuche und Koordinaten-Ermittlung
- Dokumentation: https://open-meteo.com/en/docs/geocoding-api

---

## Projektmanagement

**Methodik:** Agiles Projektmanagement (Scrum)  
**Sprint-Dauer:** 2-3 Wochen  
**Tools:** Jira (Board & Backlog), GitLab (Code & CI/CD)

### Story Points Übersicht

- **Sprint 0:** Setup & Initialisierung
- **Sprint 1:** 15 Story Points (Infrastruktur)
- **Sprint 2:** 18 Story Points (Automatisierung & Integration)
- **Sprint 3:** 16 Story Points (Code-Refactoring & UI)

**Total:** 49 Story Points

---

## Testing

### Manuelle Tests

- Standortsuche mit verschiedenen Orten
- Chart-Interaktionen und Datenfilterung
- Mobile Responsiveness
- API-Fehlerbehandlung

### Geplante Automatisierung

```python
# Beispiel: test_data_handlers.py
def test_prepare_hourly_dataframe():
    raw_data = {...}
    df = prepare_hourly_dataframe(raw_data)
    assert 'temperature_2m' in df.columns
    assert len(df) > 0
```

---

## Known Issues & Future Improvements

### Known Issues

- Streamlit ist für produktive Webauftritte nur bedingt geeignet (UI/UX-Limitierungen)
- Layout-Kontrolle über HTML/CSS ist eingeschränkt

### Geplante Verbesserungen

- Interaktive Schweizer Wetterkarte mit Leaflet
- Benachrichtigungen bei Wetteränderungen
- Historische Wetterdaten & Vergleiche
- Erweiterung auf weitere Länder
- Unit-Tests & Integration-Tests
- Migration zu React/Next.js für bessere UI-Kontrolle

---

## Lessons Learned

### Was gut funktioniert hat

- Agiles Projektmanagement mit Sprints
- Modulare Code-Architektur (Sprint 3)
- Direkte API-Integration (einfacher als CI/CD-Pipeline)
- PostgreSQL für Geodaten
- systemd-Service für stabilen Betrieb

### Herausforderungen

- Streamlit UI/UX-Limitierungen
- Design-Entscheidungen kosteten Zeit
- Initiale CI/CD-Pipeline-Planung war overengineered

### Erkenntnisse

- Einfache Lösungen bevorzugen (direkte API-Calls vs. Pipeline)
- Code-Struktur frühzeitig planen (Refactoring kostete Zeit)
- Technologie-Wahl basierend auf Anforderungen (Streamlit für MVP OK, aber nicht für Produktion)

---

## Kontakt & Projektleitung

**Robin Kiefer**  
Projektleiter, Entwickler & Administrator

**Projekttyp:** Semesterarbeit  
**Methodik:** Agiles Projektmanagement (Scrum)  
**Repository:** GitLab (privat)

---

## Lizenz

Dieses Projekt wurde als Semesterarbeit erstellt und dient Bildungszwecken.
 

