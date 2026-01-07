# SmartWeather.ch – Projektübersicht

**Projekttyp:** Semesterarbeit  
**Projektleiter:** Robin Kiefer  
**Status:** In Entwicklung  
**Projektmethode:** Agiles Projektmanagement mit Scrum

---

## Inhaltsverzeichnis

1. [Vision und Ziele](#vision-und-ziele)
2. [Projektzusammenfassung](#projektzusammenfassung)
3. [Stakeholder und Rollen](#stakeholder-und-rollen)
4. [Funktionale Anforderungen](#funktionale-anforderungen)
5. [Nicht-funktionale Anforderungen](#nicht-funktionale-anforderungen)
6. [Technologie-Stack](#technologie-stack)
7. [System-Architektur](#system-architektur)
8. [Datenbank-Design](#datenbank-design)
9. [Externe Abhängigkeiten](#externe-abhängigkeiten)
10. [Deployment und Infrastruktur](#deployment-und-infrastruktur)
11. [Sicherheitskonzept](#sicherheitskonzept)
12. [Entwicklungsprozess](#entwicklungsprozess)
13. [Sprint-Übersicht](#sprint-übersicht)
14. [Roadmap](#roadmap)
15. [Risiken und Herausforderungen](#risiken-und-herausforderungen)
16. [Erfolgsmetriken](#erfolgsmetriken)

---

## Vision und Ziele

### Projektvision

SmartWeather.ch ist eine webbasierte Wetter-Applikation, die Benutzern detaillierte und aktuelle Wetterinformationen für Schweizer Standorte bereitstellt. Die Anwendung kombiniert Echtzeit-Wetterdaten mit umfangreichen historischen Daten und Prognosen, um eine umfassende Wetterübersicht zu bieten.

### Hauptziele

| Ziel | Beschreibung | Priorität |
|------|--------------|-----------|
| **Benutzerfreundlichkeit** | Intuitive Oberfläche für schnellen Zugriff auf Wetterinformationen | Hoch |
| **Datenaktualität** | Echtzeitdaten direkt von zuverlässigen Wetter-APIs | Hoch |
| **Umfassende Visualisierung** | Interaktive Charts und Diagramme für Wetterdaten | Hoch |
| **Schweiz-Fokus** | Vollständige Abdeckung aller Schweizer Gemeinden | Mittel |
| **Produktiv-Deployment** | Stabile, öffentlich zugängliche Webanwendung | Hoch |
| **Lernziel** | Praktische Erfahrung mit modernen Web-Technologien und Infrastruktur | Hoch |

---

## Projektzusammenfassung

SmartWeather.ch ist eine moderne Wetter-Applikation, die als Semesterarbeit entwickelt wird. Das Projekt demonstriert den vollständigen Entwicklungszyklus einer Web-Applikation – von der Infrastruktur-Einrichtung über Datenbank-Design bis hin zur Frontend-Entwicklung und dem produktiven Deployment.

### Kernfunktionalitäten

- **Standortsuche:** Suche nach Schweizer Orten über eine Datenbank mit Geodaten
- **Aktuelle Wetterlage:** Echtzeit-Anzeige von Temperatur, Niederschlag, Wind, Bewölkung
- **Stundenwerte:** Detaillierte stündliche Prognosen und Historie (28 Tage)
- **Tageswerte:** Aggregierte Tageswerte mit Min/Max-Temperaturen
- **Interaktive Visualisierung:** Linien-Charts für Temperaturverläufe, Niederschlag, Wind
- **Responsive Design:** Optimiert für Desktop-Browser

### Projektumfang

- **Zeitrahmen:** 3 Sprints (Sprint 0, 1, 2 abgeschlossen)
- **Team:** 1 Person (alle Rollen)
- **Infrastruktur:** Hetzner Cloud Server (Ubuntu 22.04 LTS)
- **Domain:** smart-weather.ch mit HTTPS
- **Datenbank:** PostgreSQL mit strukturiertem Schema

---

## Stakeholder und Rollen

| Rolle | Verantwortlichkeiten | Person |
|-------|---------------------|--------|
| **Projektleiter** | Planung, Koordination, Dokumentation, Review | Robin Kiefer |
| **Entwickler** | Implementierung Backend/Frontend, API-Integration | Robin Kiefer |
| **Administrator** | Server-Setup, Infrastruktur, Deployment, Sicherheit | Robin Kiefer |
| **System** | Automatisierte Prozesse (Git-Deployment, systemd) | - |

---

## Funktionale Anforderungen

### FR-01: Standortsuche

- **Beschreibung:** Benutzer können nach Schweizer Orten suchen
- **Input:** Teilstring eines Ortsnamens
- **Output:** Wetterdaten für gefundenen Standort
- **Akzeptanzkriterien:** 
  - Fuzzy-Search funktioniert (ILIKE-Suche)
  - Koordinaten werden aus Datenbank abgerufen
  - Fehlermeldung bei nicht gefundenem Ort

### FR-02: Aktuelle Wetterdaten anzeigen

- **Beschreibung:** Dashboard mit aktuellen Wetterwerten
- **Datenpunkte:** Temperatur, Feuchte, Wind, Böen, Bewölkung, Niederschlag
- **Akzeptanzkriterien:**
  - Alle Metriken werden korrekt angezeigt
  - Werte sind formatiert (1 Dezimalstelle)
  - Icons/Emojis zur visuellen Unterstützung

### FR-03: Stündliche Übersicht

- **Beschreibung:** Tabellarische und grafische Darstellung stündlicher Werte
- **Zeitraum:** Aktueller Tag (0-24 Uhr)
- **Akzeptanzkriterien:**
  - Tabelle mit allen relevanten Parametern
  - Linien-Charts für Temperatur, Niederschlag, Wind
  - Filterung auf heutigen Tag funktioniert

### FR-04: Wettercode-Interpretation

- **Beschreibung:** WMO-Wettercodes werden visualisiert
- **Features:**
  - Icon-Mapping (0-99 → Emoji)
  - Textbeschreibungen auf Deutsch
  - Integration in Tabellen und Metriken

### FR-05: Historische Daten

- **Beschreibung:** Zugriff auf vergangene Wetterdaten
- **Zeitraum:** 14 Tage zurück
- **Status:** In Planung (zukünftige Sprints)

---

## Nicht-funktionale Anforderungen

### NFR-01: Performance

- **Anforderung:** API-Response-Zeit < 3 Sekunden
- **Maßnahmen:** Direkte API-Abfrage ohne Zwischenspeicherung
- **Messung:** Durchschnittliche Ladezeit bei Standortsuche

### NFR-02: Verfügbarkeit

- **Anforderung:** 99% Uptime
- **Maßnahmen:** 
  - systemd-Service mit automatischem Restart
  - Hetzner Cloud Infrastruktur
  - Monitoring durch systemd-Logs

### NFR-03: Sicherheit

- **Anforderung:** HTTPS-verschlüsselte Kommunikation
- **Maßnahmen:**
  - SSL-Zertifikat aktiv
  - Loadbalancer mit HTTPS-Terminierung
  - Firewall-Regeln (UFW)
  - Service-Account ohne Login-Rechte

### NFR-04: Wartbarkeit

- **Anforderung:** Code ist dokumentiert und strukturiert
- **Maßnahmen:**
  - Git-Versionierung
  - Automatisches Deployment via Git-Pull
  - Inline-Kommentare für komplexe Logik
  - **Verbesserungsbedarf:** Code-Aufteilung in Module (Sprint 3)

### NFR-05: Usability

- **Anforderung:** Intuitive Bedienung ohne Schulung
- **Maßnahmen:**
  - Klare UI-Struktur mit Spalten-Layout
  - Icons zur visuellen Orientierung
  - Fehlermeldungen bei ungültigen Eingaben

---

## Technologie-Stack

### Frontend

| Technologie | Version | Zweck |
|-------------|---------|-------|
| **Streamlit** | Latest | Web-Framework für interaktive Dashboards |
| **streamlit-calendar** | Latest | Kalender-Widget (zukünftige Features) |
| **Pandas** | Latest | Datenverarbeitung und DataFrames |

### Backend / API

| Technologie | Version | Zweck |
|-------------|---------|-------|
| **Python** | 3.12 | Programmiersprache |
| **openmeteo-requests** | Latest | Open-Meteo API Client |
| **requests-cache** | Latest | API-Request Caching |
| **retry-requests** | Latest | Automatische Wiederholungen bei Fehlern |

### Datenbank

| Technologie | Version | Zweck |
|-------------|---------|-------|
| **PostgreSQL** | 16 | Relationale Datenbank |
| **psycopg** | 3.x | Python PostgreSQL Adapter |
| **pgAdmin 4** | Latest | Datenbank-Verwaltungstool |

### Infrastruktur

| Komponente | Details |
|------------|---------|
| **Server** | Ubuntu 22.04 LTS (Hetzner Cloud) |
| **Webserver** | Streamlit (Port 8501) |
| **Reverse Proxy** | Hetzner Loadbalancer mit HTTPS |
| **Dienstverwaltung** | systemd |
| **Firewall** | UFW (Uncomplicated Firewall) |
| **Domain** | smart-weather.ch |
| **SSL** | Zertifikat von Hetzner |

### Entwicklungstools

| Tool | Zweck |
|------|-------|
| **Git / GitLab** | Versionskontrolle |
| **Jira** | Projektmanagement und Sprint-Planung |
| **PowerShell** | Remote-Administration |
| **VS Code** | Code-Editor |

---

## System-Architektur

### Architektur-Diagramm

```
┌─────────────────────────────────────────────────────────┐
│                    Benutzer (Browser)                   │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTPS
                  ▼
┌─────────────────────────────────────────────────────────┐
│            Hetzner Loadbalancer (SSL-Terminierung)      │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP (Port 8501)
                  ▼
┌─────────────────────────────────────────────────────────┐
│         Ubuntu Server (Hetzner Cloud)                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │  systemd Service: streamlit.service               │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │  Python Virtual Environment                  │  │  │
│  │  │  ├─ Streamlit App (app.py)                  │  │  │
│  │  │  ├─ Session State Management                │  │  │
│  │  │  └─ UI-Rendering                            │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  └──────────────┬─────────────────┬──────────────────┘  │
│                 │                 │                      │
│                 ▼                 ▼                      │
│  ┌──────────────────┐  ┌──────────────────────┐         │
│  │   PostgreSQL 16  │  │   Git Repository     │         │
│  │  ┌────────────┐  │  │   (Auto-Update)      │         │
│  │  │geo_location│  │  └──────────────────────┘         │
│  │  └────────────┘  │                                   │
│  └──────────────────┘                                   │
└──────────────────┬──────────────────────────────────────┘
                   │
                   │ HTTPS API Call
                   ▼
┌─────────────────────────────────────────────────────────┐
│          Open-Meteo Weather API                         │
│  (Current / Hourly / Daily Weather Data)                │
└─────────────────────────────────────────────────────────┘
```

### Datenfluss

1. **Benutzer-Anfrage:**
   - Benutzer gibt Ortsnamen ein
   - Streamlit sendet Suchanfrage

2. **Standort-Resolution:**
   - Query gegen PostgreSQL geo_location Tabelle
   - ILIKE-Suche für flexible Eingaben
   - Rückgabe von Latitude/Longitude

3. **Wetterdaten-Abfrage:**
   - API-Request an Open-Meteo mit Koordinaten
   - Parameter: current, hourly (28 Tage), daily (28 Tage)
   - JSON-Response wird empfangen

4. **Daten-Processing:**
   - Pandas DataFrames für Zeitreihen
   - Filterung auf aktuellen Tag
   - Berechnungen (z.B. Temperatur-Delta)

5. **Visualisierung:**
   - Session State speichert verarbeitete Daten
   - Metriken, Tabellen und Charts werden gerendert
   - UI-Update ohne Page-Reload

---

## Datenbank-Design

### Entity Relationship Model

```
geo_location (1) ──< (n) weather_current
            (1) ──< (n) weather_hourly
            (1) ──< (n) weather_daily
```

### Tabellen-Schema

#### geo_location

```sql
CREATE TABLE geo_location (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    canton TEXT,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    elevation INTEGER,
    feature_code TEXT,
    UNIQUE (latitude, longitude)
);
```

**Zweck:** Zentrale Referenztabelle für Schweizer Ortschaften mit Geodaten

#### weather_current, weather_hourly, weather_daily

**Design-Prinzipien:**
- Composite Primary Keys: (latitude, longitude, time/day)
- Foreign Keys zu geo_location
- UPSERT-fähig über UNIQUE Constraints
- Normalisiert nach Granularität

**Status:** Tabellen existieren, werden aktuell nicht befüllt (API-Daten werden nur in Session State gehalten)

---

## Externe Abhängigkeiten

### Open-Meteo Weather API

- **URL:** https://api.open-meteo.com/v1/forecast
- **Dokumentation:** https://open-meteo.com/en/docs
- **Lizenz:** Open-Source, kostenlos nutzbar
- **Rate Limits:** 10.000 Requests/Tag (ausreichend)
- **Verfügbarkeit:** 99.9% Uptime

**Verwendete Endpunkte:**
- `/v1/forecast` – Wetter-Forecasts und Historie
- `/v1/search` (Geocoding) – für initiale Geodaten-Befüllung

**Abgerufene Parameter:**
- Current: 15 Parameter (Temperatur, Wind, Niederschlag, etc.)
- Hourly: 42 Parameter (inkl. Bodendaten, mehrere Höhen)
- Daily: 23 Parameter (Aggregierte Tageswerte)

---

## Deployment und Infrastruktur

### Server-Konfiguration

| Parameter | Wert |
|-----------|------|
| **Provider** | Hetzner Cloud |
| **Server-Typ** | Shared vCPU |
| **OS** | Ubuntu 22.04 LTS |
| **IP-Adresse** | 49.13.117.52 |
| **Hostname** | host.smart-ch.ch |

### Deployment-Prozess

1. **Manueller Deploy:**
   - systemd Service-Restart: `sudo systemctl restart streamlit`
   - Git-Pull erfolgt automatisch beim Start via Startskript

2. **Startskript-Mechanismus:**
   ```bash
   /usr/local/bin/run_smartweather.sh
   ├─ Git fetch origin main
   ├─ Git checkout app.py
   ├─ Copy app.py to deploy directory
   └─ Start Streamlit
   ```

3. **Service-Management:**
   - Service: `streamlit.service`
   - User: `streamlit` (Service-Account)
   - Auto-Restart: `Restart=always`

### Netzwerk-Konfiguration

- **Firewall (UFW):**
  - Port 22 (SSH)
  - Port 8501 (Streamlit)
  - Port 5432 (PostgreSQL - eingeschränkt)

- **Loadbalancer:**
  - HTTPS (443) → Server Port 8501
  - SSL-Zertifikat aktiv
  - Automatisches Failover (Hetzner)

---

## Sicherheitskonzept

### Authentifizierung

- **Aktuell:** Keine Benutzer-Authentifizierung (Public App)
- **Datenbank:** Passwort-geschützt (SCRAM-SHA-256)
- **Server:** SSH-Key basierter Zugriff

### Autorisierung

- **Service-Account:** `streamlit` User ohne Shell-Zugriff
- **File Permissions:** 750 für App-Verzeichnisse
- **Database Roles:** Dedizierter `dbadm_robin` User

### Netzwerksicherheit

- **HTTPS-Verschlüsselung:** Alle externen Verbindungen
- **Firewall:** Restriktive UFW-Regeln
- **SSH:** Key-basiert, kein Password-Login
- **Git:** Deploy-Key (Read-Only) für Repository

### Datenschutz

- **Keine personenbezogenen Daten:** App speichert keine Benutzerdaten
- **Session State:** Nur temporär während Browser-Session
- **Logs:** Keine sensiblen Informationen in Logs

---

## Entwicklungsprozess

### Agile Methodik (Scrum)

- **Sprint-Dauer:** Flexibel (ca. 1-2 Wochen)
- **Rollen:** Alle Rollen durch eine Person (Robin Kiefer)
- **Artefakte:** 
  - Product Backlog (Jira)
  - Sprint Backlog (Jira)
  - Project Workbook (Markdown)

### Workflow

1. **Sprint Planning:** Definition von User Stories und Tasks in Jira
2. **Development:** Implementierung in lokaler Umgebung
3. **Testing:** Manuelle Tests der Funktionalität
4. **Deployment:** Git-Push → Server-Restart
5. **Review:** Überprüfung der Deliverables
6. **Retrospektive:** Lessons Learned dokumentieren

### Git-Strategie

- **Branch-Modell:** Simplified Git Flow (main Branch)
- **Commits:** Feature-basiert mit beschreibenden Messages
- **Repository:** GitLab (hf9064413/smart-weather.ch_semesterrarbeit02)

---

## Sprint-Übersicht

### Sprint 0: Projektinitialisierung & Setup

**Ziel:** Grundlagen schaffen

**Deliverables:**
- GitLab Repository erstellt
- Jira Workspace eingerichtet
- Hetzner Account bereit
- Basis-Dokumentation

**Status:** Abgeschlossen

---

### Sprint 1: Server & Infrastruktur

**Ziel:** Produktive Infrastruktur aufsetzen

**Deliverables:**
- Ubuntu Server auf Hetzner
- Domain smart-weather.ch mit HTTPS
- PostgreSQL Datenbank installiert
- Streamlit als Test-App deployed
- Firewall und Sicherheit konfiguriert

**Status:** Abgeschlossen

---

### Sprint 2: Automatisierung & Integration

**Ziel:** Wetterdaten-App mit Live-Daten

**Deliverables:**
- Streamlit als systemd-Dienst
- Git-Integration mit Auto-Update
- Datenbank-Schema mit geo_location
- Vollständige Wetter-Visualisierung
- Direkte API-Integration

**Highlights:**
- Architekturentscheidung: Keine Pipeline, direkte API
- Umfangreiches Dashboard mit Charts
- 650+ Zeilen Code in app.py

**Status:** Abgeschlossen

**Lessons Learned:**
- Design-Entscheidungen früher treffen
- Code-Struktur wird zu monolithisch → Refactoring nötig

---

## Roadmap

### Sprint 3: Code-Refactoring & Features (Geplant)

**Ziele:**
- app.py in Module aufteilen
  - `ui_components.py` – Wiederverwendbare UI-Elemente
  - `data_handlers.py` – Daten-Processing Funktionen
  - `api_client.py` – API-Kommunikation
  - `database.py` – Datenbank-Queries
- Wiederverwendbare Funktionen für repetitive Blöcke
- Kalender-Funktionalität implementieren (Tagesselektion)
- Error-Handling verbessern

**Erwartete Verbesserungen:**
- Bessere Wartbarkeit
- Einfacheres Testing
- Schnellere Feature-Entwicklung

---

### Sprint 4: Erweiterte Features (Geplant)

**Mögliche Features:**
- Historische Daten-Ansicht (14 Tage zurück)
- Vergleich mehrerer Standorte
- Export-Funktion (CSV/PDF)
- Favoriten-Standorte speichern
- Push-Benachrichtigungen bei Wetterwarnungen

---

### Sprint 5: Optimierung & Polish (Geplant)

**Ziele:**
- Performance-Optimierung
- Mobile-Optimierung
- Erweiterte Visualisierungen
- Benutzerdokumentation
- Abschluss-Präsentation vorbereiten

---

## Risiken und Herausforderungen

### Technische Risiken

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| **API-Verfügbarkeit** | Niedrig | Hoch | Retry-Mechanismus, Error-Handling |
| **Server-Ausfall** | Niedrig | Mittel | systemd Auto-Restart, Hetzner SLA |
| **Datenbank-Performance** | Niedrig | Mittel | Indexierung, Query-Optimierung |
| **Code-Komplexität** | Hoch | Mittel | Geplantes Refactoring in Sprint 3 |

### Projekt-Risiken

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| **Zeitüberschreitung** | Mittel | Hoch | Priorisierung, MVP-Fokus |
| **Scope Creep** | Mittel | Mittel | Klare Sprint-Ziele, Backlog-Priorisierung |
| **Fehlende Skills** | Niedrig | Mittel | Dokumentation, Online-Ressourcen |

### Bisherige Herausforderungen

- **Design-Entscheidungen:** Mehrfache UI-Überarbeitungen
- **Architektur-Wechsel:** Pipeline → direkte API (erfolgreich gelöst)
- **Code-Wartbarkeit:** Wachsende Komplexität in app.py (Sprint 3 geplant)

---

## Erfolgsmetriken

### Technische Metriken

| Metrik | Zielwert | Aktuell | Status |
|--------|----------|---------|--------|
| **Uptime** | > 99% | ~99.5% | OK |
| **API Response Time** | < 3s | ~2s | OK |
| **Code Coverage (Tests)** | > 70% | 0% | Geplant |
| **Deployment-Zeit** | < 5 min | ~2 min | OK |

### Projekt-Metriken

| Metrik | Zielwert | Aktuell | Status |
|--------|----------|---------|--------|
| **Abgeschlossene Sprints** | 5 | 3 | In Arbeit |
| **Dokumentierte User Stories** | 15+ | 12 | OK |
| **Deliverables erreicht** | 100% | 100% | OK |
| **Code-Zeilen** | - | 650+ | - |

### Lernziele

- [X] Cloud-Infrastruktur (Hetzner)
- [X] Linux Server-Administration
- [X] PostgreSQL Datenbank-Design
- [X] Streamlit Web-Framework
- [X] API-Integration
- [X] systemd Service-Management
- [X] Git-basiertes Deployment
- [ ] Code-Architektur (Refactoring geplant)
- [ ] Agiles Projektmanagement

---

## Zusammenfassung

SmartWeather.ch demonstriert erfolgreich die Entwicklung einer produktiven Web-Applikation mit modernem Technologie-Stack. Das Projekt zeigt:

- **Vollständiger DevOps-Zyklus:** Von Infrastruktur bis Deployment
- **Agile Entwicklung:** Strukturierte Sprints mit klaren Deliverables
- **Technische Vielfalt:** Server, Datenbank, API, Frontend
- **Praktische Anwendung:** Echte Wetterdaten für reale Nutzung
- **Kontinuierliche Verbesserung:** Lessons Learned werden umgesetzt

Das Projekt ist aktuell produktiv unter https://smart-weather.ch erreichbar und wird in den kommenden Sprints weiterentwickelt.

---

**Letzte Aktualisierung:** Januar 2026  
**Dokumentversion:** 1.0  
**Kontakt:** Robin Kiefer
