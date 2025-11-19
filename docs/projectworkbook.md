# Projektdokumentation

**Projektleiter:** Robin Kiefer
**Projekt:** SmartWeather.ch

## Legende

Die Sprints bestehen aus Stories welche gleichzeitig die Auszuführenden Tasks sind und diese zusammengesetzt in einer Epic welche als Meilenstein dient.

## Introduction


-	Entwicklung eines Python-Skripts, das Wetterdaten (z.B. OpenWeatherMap) abruft und verarbeitet.

-	Aufbau einer Supabase-Datenbank inkl. API-Integration zur Speicherung der Wetterdaten.

-	Einrichtung einer GitLab CI/CD Pipeline, die das Python-Skript automatisiert ausführt und die Daten aktualisiert.

-	Implementierung einer Streamlit-Webanwendung zur Visualisierung der gesammelten Wetterdaten.

-	Optional: Erweiterung um Funktionen wie Vergleich mehrerer Orte oder Benachrichtigungen bei Extremwetter.


---

## 2. Systemübersicht

| Komponente        | Beschreibung                                        |
| ----------------- | --------------------------------------------------- |
| Hostsystem        | Ubuntu Server 22.04 LTS                             |
| Datenbankdienst   | PostgreSQL Version 16                               |
| Verwaltungstools  | pgAdmin 4, PowerShell mit psql                      |
| Zugriff           | Lokal und Remote über Port 5432                     |
| Authentifizierung | SCRAM-SHA-256                                       |
| Benutzer          | dbadm_robin                                         |
| Datenbank         | smartweatherdb                                      |
| DNS               | host.smart-ch.ch (A-Record), db.smart-ch.ch (CNAME) |
| IP-Adresse        | 49.13.117.52                                        |
| Firewall          | UFW mit eingeschränkten Regeln                      

# Sprint 0 – Projektinitialisierung & Setup

## Ziel des Sprints

Eine lauffähige Entwicklungsumgebung und Basis-Projektstruktur bereitstellen, um in Sprint 1 mit der eigentlichen Funktionalität beginnen zu können.

---

## 1. Epics und User Stories

| Epic (Key)                              | Story-ID | Rolle         | Ziel                                                                                      | Nutzen                                                               | Akzeptanzkriterien                                                                                               |
| --------------------------------------- | -------- | ------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| SCRUM-19 Projektinitialisierung & Setup | SCRUM-33 | Projektleiter | Eine Dokumentation haben                                                                  | Projektverlauf und Entscheidungen sind nachvollziehbar               | Es existiert eine strukturierte Projektdokumentation (z. B. Sprintberichte, Installationsdoku) im Repository     |
| SCRUM-19 Projektinitialisierung & Setup | SCRUM-20 | Entwickler    | Eine klare Projektstruktur und ein Git-Repository haben                                   | Einheitliche Basis für die Entwicklung                               | Git-Repo ist erstellt und enthaelt mindestens `app.py`, `.gitignore`, `README.md`                                |
| SCRUM-19 Projektinitialisierung & Setup | SCRUM-21 | Entwickler    | Ein Hetzner Konto haben, um dort Maschinen zu hosten und Netzwerkkomponenten zu verwalten | Infrastruktur fuer das spaetere Hosting der Applikation steht bereit | Hetzner Account ist erstellt, Login getestet, erste Ressourcen koennen angelegt werden                           |
| SCRUM-19 Projektinitialisierung & Setup | SCRUM-22 | Entwickler    | Einen Jira Workspace eingerichtet haben, damit ich die PL machen kann                     | Planung und Nachverfolgung der Arbeit ist zentral moeglich           | Jira-Projekt ist erstellt, Board und Sprint 0 sind konfiguriert, Zugriff fuer Projektbeteiligte ist eingerichtet |

---

## 3. Aufgaben (Tasks)

| ID   | Beschreibung              | Zugeordnet zu Story | Verantwortlich | Status |
| ---- | ------------------------- | ------------------- | -------------- | ------ |
| T-01 | Dokumentation erstellen   | SCRUM-33            | Robin          | To Do  |
| T-02 | GitLab Repo erstellen     | SCRUM-20            | Robin          | To Do  |
| T-03 | Hetzner Account erstellen | SCRUM-21            | Robin          | To Do  |
| T-04 | Kreditkarte hinterlegen   | SCRUM-21            | Robin          | To Do  |
| T-05 | Jira Workspace erstellen  | SCRUM-22            | Robin          | To Do  |


---

## 4. Deliverables (Ergebnisse)

| Nr. | Deliverable                 | Bezug Story | Beschreibung                                                                                        | Nachweis / Artefakt                                                              |
| --- | --------------------------- | ----------- | --------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| 1   | Projektdokumentation        | SCRUM-33    | Grundlage der Dokumentation ist erstellt (z. B. Einleitung, Vorgehen, Sprint 0, Installationsdoku). | Dateien wie `projectworkbook.md`       |
| 2   | GitLab Repository           | SCRUM-20    | GitLab Repo ist erstellt, Projektstruktur angelegt, initialer Commit erfolgt.                       | GitLab Projekt-URL, Commit-Log, Struktur mit `app.py`, `.gitignore`, `README.md` |
| 3   | Hetzner Account bereit      | SCRUM-21    | Hetzner Konto existiert, Login getestet, Kreditkarte hinterlegt, Account einsatzbereit für Server.  | Screenshot Kontoübersicht / Billing, ggf. Notiz „Login getestet am <Datum>“      |
| 4   | Jira Workspace eingerichtet | SCRUM-22    | Jira Projekt für die Semesterarbeit erstellt, Board und Sprint 0 konfiguriert.                      | Screenshot des Jira Boards mit Sprint 0 und den Issues SCRUM-20, 21, 22, 33      |


---

## 5. Fortschritt

| Kennzahl     | Geplant | Erreicht |
| ------------ | ------- | -------- |
| Story Points | [x]     | [y]      |
| Aufgaben     | [x]     | [y]      |

---

## 6. Review

Kurze Zusammenfassung, was in diesem Sprint umgesetzt wurde.
Beispiel:

* Streamlit-Setup abgeschlossen
* App läuft lokal
* Git-Repository initialisiert

---

## 7. Retrospektive

| Frage                                      | Antwort |
| ------------------------------------------ | ------- |
| Was lief gut?                              | ...     |
| Was war schwierig?                         | ...     |
| Was kann verbessert werden?                | ...     |
| Was nehmen wir mit in den nächsten Sprint? | ...     |

---

## 8. Planung Nächster Sprint

| Bereich        | Ziel |
| -------------- | ---- |
| Funktionalität | ...  |
| Technik        | ...  |
| Organisation   | ...  |

---

## 9. Worklog

Hier dokumentierst du **konkrete Arbeitsschritte, Code und Tests** – ideal, um technische Nachweise zu liefern.

### Datum: [TT.MM.YYYY]

**Aktivität:** Umgebung erstellt
**Befehle:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install streamlit
```

**Ergebnis:**

```bash
streamlit --version
# Streamlit, version 1.39.0
```

---

### Datum: [TT.MM.YYYY]

**Aktivität:** App gestartet
**Code:**

```python
import streamlit as st

st.title("Wetter App")
st.write("Dies ist ein Testlauf der Basis-App.")
```

**Befehl zum Starten:**

```bash
streamlit run app.py
```

**Ergebnis:**
App läuft lokal auf [http://localhost:8501](http://localhost:8501)

---

Möchtest du, dass ich dir diese Struktur gleich als **Markdown-Datei (`SPRINT_TEMPLATE.md`)** exportiere, damit du sie direkt in dein Repository legen kannst und pro Sprint kopierst (z. B. `SPRINT0.md`, `SPRINT1.md` usw.)?
