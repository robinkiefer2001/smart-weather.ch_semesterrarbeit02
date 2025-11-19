# Projektdokumentation

## Sprint1 Aufbau eines PostgreSQL-Datenbankservers auf Ubuntu

**Projektleiter:** Robin Kiefer
**Projekt:** SmartWeather.ch

---

## 1. Zielsetzung

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
| Firewall          | UFW mit eingeschränkten Regeln                      |

---

## 3. Konfiguration von Ubuntu Server

### 3.1 Systemaktualisierung

```
sudo apt update && sudo apt full-upgrade -y
```

### 3.2 Grundlegende Tools

```
sudo apt install -y vim htop curl wget git ufw fail2ban net-tools
```

### 3.3 PostgreSQL-Repository

```
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
sudo apt update
sudo apt install -y postgresql postgresql-contrib
```

### 3.4 Dienstaktivierung

```
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

---

## 4. Benutzer- und Datenbankeinrichtung

```
sudo -u postgres psql
CREATE USER dbadm_robin WITH PASSWORD 'xxxxxxxxx';
CREATE DATABASE smartweatherdb OWNER dbadm_robin;
GRANT ALL PRIVILEGES ON DATABASE smartweatherdb TO dbadm_robin;
\q
```

---

## 5. Konfiguration Postgres

### 5.1 postgresql.conf

Datei: `/etc/postgresql/16/main/postgresql.conf`

```
listen_addresses = '*'
port = 5432
logging_collector = on
log_connections = on
log_disconnections = on
```

### 5.2 pg_hba.conf

Datei: `/etc/postgresql/16/main/pg_hba.conf`

```
local   all             all                                     scram-sha-256
host    all             all             0.0.0.0/0               scram-sha-256
host    all             all             ::1/128                 scram-sha-256
local   replication     all                                     scram-sha-256
host    replication     all             127.0.0.1/32            scram-sha-256
host    replication     all             ::1/128                 scram-sha-256
```

### 5.3 Dienstneustart

```
sudo systemctl restart postgresql
```

---

## 6. Firewall

```
sudo ufw allow OpenSSH
sudo ufw allow 5432/tcp
sudo ufw enable
sudo ufw status verbose
```
---

## 7. DNS-Konfiguration

Die Domäne ist gekauft, von Swizzonic dort habe ich die DNS-Einträge hinterlegt für die Zukünftige Website.

Domain: `smart-ch.ch`

```
A-Record: host.smart-ch.ch -> 49.13.117.52
CNAME: db.smart-ch.ch -> host.smart-ch.ch
```

---

## 8. Verbindungstests

### 8.1 Lokal

```
psql -U dbadm_robin -d smartweatherdb -W
```

### 8.2 Remote

```
psql -h 49.13.117.52 -U dbadm_robin -d smartweatherdb -W
```

### 8.3 Firewalltest unter Windows

```
Test-NetConnection -ComputerName 49.13.117.52 -Port 5432
```

---

## 9. pgAdmin-Verbindung

**Parameter:**

| Feld           | Wert                |
| -------------- | ------------------- |
| Name           | RKI-UbuntuSrv001      |
| Host           | db.smart-ch.ch      |
| Port           | 5432                |
| Maintenance DB | postgres      |
| Username       | dbadm_robin         |
| Password       | Passwort            |
| SSL Mode       | Prefer oder Disable |

---

<<<<<<< HEAD
streamlist in /opt
adm_rki@RKI-UBUSRV001:/opt/streamlit$ source ./venv/bin/activate
(venv) adm_rki@RKI-UBUSRV001:/opt/streamlit$
=======
Klar. Hier ist deine saubere, technisch präzise Projektdokumentation ohne Symbole oder Beispielausgaben:

---

# Projektdokumentation

## Aufbau eines PostgreSQL-Datenbankservers auf Ubuntu

**Projektleiter:** Robin Kiefer
**Rolle:** IT System Engineer / Netzwerkspezialist
**Projekt:** SmartWeatherDB

---

## 1. Zielsetzung

Einrichtung eines sicheren und administrierbaren PostgreSQL-Datenbankservers auf Ubuntu Server.
Ziel ist ein stabiler, netzwerkfähiger Datenbankdienst mit sicherer Authentifizierung und Remote-Zugriff über pgAdmin.

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
| Firewall          | UFW mit eingeschränkten Regeln                      |

---

## 3. Installation

### 3.1 Systemaktualisierung

```
sudo apt update && sudo apt full-upgrade -y
```

### 3.2 Grundlegende Tools

```
sudo apt install -y vim htop curl wget git ufw fail2ban net-tools
```

### 3.3 PostgreSQL-Repository

```
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
sudo apt update
sudo apt install -y postgresql postgresql-contrib
```

### 3.4 Dienstaktivierung

```
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

---

## 4. Benutzer- und Datenbankeinrichtung

```
sudo -u postgres psql
CREATE USER dbadm_robin WITH PASSWORD 'Qwer123*!';
CREATE DATABASE smartweatherdb OWNER dbadm_robin;
GRANT ALL PRIVILEGES ON DATABASE smartweatherdb TO dbadm_robin;
\q
```

---

## 5. Konfiguration

### 5.1 postgresql.conf

Datei: `/etc/postgresql/16/main/postgresql.conf`

```
listen_addresses = '*'
port = 5432
logging_collector = on
log_connections = on
log_disconnections = on
```

### 5.2 pg_hba.conf

Datei: `/etc/postgresql/16/main/pg_hba.conf`

```
local   all             all                                     scram-sha-256
host    all             all             0.0.0.0/0               scram-sha-256
host    all             all             ::1/128                 scram-sha-256
local   replication     all                                     scram-sha-256
host    replication     all             127.0.0.1/32            scram-sha-256
host    replication     all             ::1/128                 scram-sha-256
```

### 5.3 Dienstneustart

```
sudo systemctl restart postgresql
```

---

## 6. Firewall

```
sudo ufw allow OpenSSH
sudo ufw allow 5432/tcp
sudo ufw enable
sudo ufw status verbose
```

Empfohlene Einschränkung nach Testphase:

```
sudo ufw delete allow 5432/tcp
sudo ufw allow from 192.168.1.0/24 to any port 5432 proto tcp
```

---

## 7. DNS-Konfiguration

Domain: `smart-ch.ch`

```
A-Record: host.smart-ch.ch -> 49.13.117.52
CNAME: db.smart-ch.ch -> host.smart-ch.ch
```

---

## 8. Verbindungstests

### 8.1 Lokal

```
psql -U dbadm_robin -d smartweatherdb -W
```

### 8.2 Remote

```
psql -h 49.13.117.52 -U dbadm_robin -d smartweatherdb -W
```

### 8.3 Firewalltest unter Windows

```
Test-NetConnection -ComputerName 49.13.117.52 -Port 5432
```

---

## 9. pgAdmin-Verbindung

**Parameter:**

| Feld           | Wert                |
| -------------- | ------------------- |
| Name           | SmartWeatherDB      |
| Host           | db.smart-ch.ch      |
| Port           | 5432                |
| Maintenance DB | smartweatherdb      |
| Username       | dbadm_robin         |
| Password       | Passwort            |
| SSL Mode       | Prefer oder Disable |

---


# Installation und Konfiguration von Streamlit auf Ubuntu Server

## Systemvorbereitung

### Systemaktualisierung
```

sudo apt update && sudo apt upgrade -y

```

### Installation von Python, Pip und venv
```

sudo apt install -y python3 python3-pip python3-venv

```

### Erstellung eines Projektverzeichnisses
```

sudo mkdir -p /opt/streamlit
sudo chown $USER:$USER /opt/streamlit
cd /opt/streamlit

```

## Virtuelle Umgebung

### Erstellung einer virtuellen Python-Umgebung
```

python3 -m venv venv

```

### Aktivierung
```

source venv/bin/activate

```

## Installation von Streamlit

### Aktualisierung von Pip und Installation
```

pip install --upgrade pip
pip install streamlit

```

### Prüfung der Installation
```

streamlit --version

```

## Beispielanwendung

### Erstellung einer Datei app.py im Projektverzeichnis
```

nano app.py

````

### Inhalt
```python
import streamlit as st

st.title("Streamlit Server Test")
st.write("Der Streamlit Server läuft erfolgreich auf Ubuntu.")
````

## Start der Anwendung

### Startbefehl

```
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

## Firewallkonfiguration

### Freigabe von Port 8501

```
sudo ufw allow 8501/tcp
```

### Überprüfung der Firewallregeln

```
sudo ufw status verbose
```

## Automatischer Start als Systemdienst

### Erstellung einer Systemd-Service-Datei

```
sudo nano /etc/systemd/system/streamlit.service
```

### Inhalt

```
[Unit]
Description=Streamlit App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/streamlit
ExecStart=/opt/streamlit/venv/bin/streamlit run /opt/streamlit/app.py --server.address=0.0.0.0 --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

### Aktivierung und Start

```
sudo systemctl daemon-reload
sudo systemctl enable streamlit
sudo systemctl start streamlit
sudo systemctl status streamlit
```

>>>>>>> 757c4c41703a19e4ae3406e0348c5e165d6e7129
