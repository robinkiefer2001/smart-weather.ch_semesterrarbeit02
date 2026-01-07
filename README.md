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
| Sprint 2 | Abgeschlossen | systemd-Service, Git-Integration, Wetterdaten-Visualisierung |
| Sprint 3 | Geplant | Code-Refactoring, Module, erweiterte Features |

**Aktuelle Version:** Sprint 2 (Januar 2026)

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
 

