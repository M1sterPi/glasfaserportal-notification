# Glasfaserportal-Notification
Ein automatisches Überwachungstool für das Telekom Glasfaser-Portal. Dieses Skript prüft regelmäßig, ob sich der Status Ihres Glasfaserausbaus geändert hat und sendet Ihnen eine E-Mail-Benachrichtigung, sobald Änderungen erkannt werden.

## Funktionen
🔍 Überwacht automatisch den Status Ihres Glasfaseranschlusses
📧 Sendet E-Mail-Benachrichtigungen bei Statusänderungen
🤖 Lässt sich mit GitHub Actions vollständig automatisieren
🔄 Verfolgt Änderungen am "Aktuelle Informationen"-Abschnitt und am Status-Tracker

## Installation
1. Repository klonen:
git clone https://github.com/M1sterPi/glasfaserportal-notification.git
cd glasfaserportal-notification

2. Python-Abhängigkeiten installieren:
pip install -r requirements.txt

3. Playwright-Browser installieren:
python -m playwright install firefox

## Konfiguration
 
1. Erstellen Sie eine .env-Datei im Projektverzeichnis mit folgenden Inhalten:

### Telekom-Portal
FIBER_STATUS_URL=https://glasfaser.telekom.de/glasfaser-portal/?token=IHR_TOKEN_HIER

### SMTP-Zugang
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=ihre.email@gmail.com
SMTP_PASS=ihr_app_passwort
SMTP_TO=empfaenger@example.com

2. Ersetzen Sie IHR_TOKEN_HIER mit Ihrem persönlichen Token aus der Telekom-Portal-URL.

3. Für Gmail müssen Sie ein App-Passwort erstellen unter: Google Account → Sicherheit → 2-Faktor → App-Passwörter


## Manuelle Ausführung
python glasfaserportal_notification.py

Automatisierung mit GitHub Actions
Das Repository enthält bereits eine GitHub Actions Workflow-Datei, die das Skript regelmäßig ausführt. Folgen Sie diesen Schritten, um die Automatisierung einzurichten:

1. Forken Sie dieses Repository oder pushen Sie es in Ihr eigenes GitHub-Repository.

2. Fügen Sie in Ihrem GitHub-Repository unter "Settings" → "Secrets and variables" → "Actions" folgende Repository Secrets hinzu:

FIBER_STATUS_URL: Die URL zum Telekom Glasfaser-Portal mit Ihrem Token
SMTP_HOST: Ihr SMTP-Server (Standard: smtp.gmail.com)
SMTP_PORT: Ihr SMTP-Port (Standard: 587)
SMTP_USER: Ihre E-Mail-Adresse
SMTP_PASS: Ihr E-Mail-Passwort oder App-Passwort
SMTP_TO: Empfänger-E-Mail (optional, wenn abweichend)
Der Workflow wird automatisch alle 5 Minuten ausgeführt (kann in der run-script.yml angepasst werden).

## Funktionsweise
Das Skript öffnet das Telekom Glasfaser-Portal in einem virtuellen Browser
Es extrahiert den "Aktuelle Informationen"-Abschnitt und den Status der Fortschrittsanzeige
Diese Informationen werden in einen Hash umgewandelt
Bei Änderungen im Vergleich zum vorherigen Hash wird eine E-Mail gesendet

## Mitwirken
Beiträge, Problemmeldungen und Verbesserungsvorschläge sind willkommen! Öffnen Sie einfach ein Issue oder Pull Request.


