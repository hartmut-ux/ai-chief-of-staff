# Schritt-für-Schritt: Chief of Staff mit Kimi Code CLI bei dir aufsetzen

Diese Anleitung führt dich persönlich durch die Installation und Konfiguration des AI Chief of Staff auf deinem Mac, speziell für **Kimi Code CLI**.

> **Ziel am Ende:** Du gibst in Kimi `/chief-of-staff` ein und erhältst jeden Morgen ein priorisiertes Briefing aus deinen E-Mails, Kalender, Tasks und Web-Signalen — mit vorgeschlagenen Aktionen, die du einfach freigibst.

---

## Voraussetzungen

- Mac mit macOS (du arbeitest auf einem Mac).
- **Kimi Code CLI** ist installiert und läuft im Terminal oder in VS Code.
- Python 3.10 oder höher ist installiert (`python3 --version` im Terminal prüfen).
- Du hast Zugriff auf ein Terminal und einen Texteditor (VS Code, Cursor, Zed oder `nano`).

---

## Schritt 1: Repository klonen

Öffne das Terminal und wechsle in einen Ordner, in dem du deine Projekte ablegst (z. B. `~/Documents`):

```bash
cd ~/Documents
git clone https://github.com/hartmut-ux/ai-chief-of-staff.git
cd ai-chief-of-staff
```

> Tipp: Wenn du das Projekt woanders speicherst, passe die Pfade in dieser Anleitung entsprechend an.

---

## Schritt 2: Python-Abhängigkeiten installieren

Im Projektordner ausführen:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Wenn `requirements.txt` fehlt oder leer ist, installiere mindestens:

```bash
pip install python-dotenv toml jinja2
```

---

## Schritt 3: Interaktiven Installer starten

Der Installer fragt dich, welche Quellen und Ausgabe-Kanäle du aktivieren möchtest, und legt die Grundkonfiguration an:

```bash
python3 scripts/install.py
```

Wähle im Installer:

1. **Assistant:** `Kimi Code CLI`
2. **Sources:** Empfohlen für den Start: `email`, `calendar`, `tasks`, `web`
3. **Delivery channels:** Empfohlen für den Start: `console` (Terminal) — später kannst du Slack, E-Mail oder Notion hinzufügen
4. **Approval level:** `draft` (sicherer Start: Briefing wird nur angezeigt, nichts wird automatisch gesendet)

Der Installer erstellt:

- `.env` aus der Vorlage `.env.example`
- `config/chief_of_staff.toml` mit deinen Einstellungen

---

## Schritt 4: `.env` mit deinen Zugangsdaten füllen

Öffne `.env` im Editor und trage mindestens ein:

```bash
# Kimi / LLM
OPENAI_API_KEY=sk-...
KIMI_API_KEY=...

# MCP-Server-Namen (so, wie du sie später in Kimi registrierst)
GMAIL_MCP_NAME=gmail
CALENDAR_MCP_NAME=calendar
NOTION_MCP_NAME=notion
SLACK_MCP_NAME=slack
```

> **Wichtig:** `.env` wird von Git ignoriert. Speichere dort niemals echte Secrets ab, bevor du sicher bist, dass die Datei nicht committed wird.

---

## Schritt 5: MCP-Server in Kimi registrieren

Kimi spricht mit Gmail, Kalender, Notion und Slack über **MCP-Server**. Du musst sie einmalig in Kimi registrieren.

```bash
kimi mcp add gmail      --command "npx -y @anthropic-ai/mcp-gmail"
kimi mcp add calendar   --command "npx -y @anthropic-ai/mcp-calendar"
kimi mcp add notion     --command "npx -y @anthropic-ai/mcp-notion"
kimi mcp add slack      --command "npx -y @anthropic-ai/mcp-slack"
```

Die genauen Paketnamen können je nachdem variieren, welchen MCP-Server du verwendest. Siehe [docs/mcp-setup.md](mcp-setup.md) für:

- Gmail OAuth2 in der Google Cloud Console
- Google Calendar OAuth2
- Notion Integration Token und Datenbank-ID
- Slack Incoming Webhook

> **Hinweis:** Wenn du noch keine OAuth-Credentials hast, starte mit `web` als einzige aktivierte Quelle, um das Briefing-Format zu testen. Du kannst E-Mail und Kalender später nachrüsten.

---

## Schritt 6: Skill in Kimi bekannt machen

Kimi lädt Skills aus dem `.kimi/skills/`-Ordner. Da der Skill bereits im Repo liegt (`ai-chief-of-staff/.kimi/skills/chief-of-staff/SKILL.md`), musst du Kimi nur mitteilen, wo sich dein Projektordner befindet.

**Option A — im aktuellen Arbeitsbereich:**

Starte Kimi Code CLI direkt im Projektordner:

```bash
cd ~/Documents/ai-chief-of-staff
kimi
```

Dann sollte der Skill automatisch erkannt werden.

**Option B — global verfügbar machen:**

Kopiere oder verlinke den Skill-Ordner in Kimis globales Skills-Verzeichnis. Der Pfad hängt von deiner Kimi-Installation ab, typischerweise:

```bash
mkdir -p ~/.kimi/skills
cp -R .kimi/skills/chief-of-staff ~/.kimi/skills/
```

> Falls der Pfad bei dir anders ist, prüfe `kimi config` oder die Kimi-Dokumentation.

---

## Schritt 7: Ersten Testlauf machen

Starte im Projektordner:

```bash
python3 -m chief_of_staff run --preview
```

Du solltest jetzt ein erstes Briefing im Terminal sehen. Im Start-Modus werden nur die Quellen genutzt, die du konfiguriert hast, und nichts wird versendet (weil `approval = "draft"`).

Wenn Fehler auftreten:

- Prüfe, ob die MCP-Server in Kimi korrekt registriert sind (`kimi mcp list`).
- Vergleiche die Namen in `.env` (`GMAIL_MCP_NAME` etc.) mit den registrierten Namen.
- Siehe die Fehlertabelle in [docs/mcp-setup.md](mcp-setup.md).

---

## Schritt 8: Persönliche Präferenzen eintragen

Öffne `memory/preferences.md` und ergänze:

- Aktuelle Projekte und Ziele
- Wichtige Kunden oder Investoren
- Themen, die immer priorisiert werden sollen
- Themen, die ignoriert werden sollen
- Bevorzugte Tonfall und Länge des Briefings

Öffne `constitution.md` und passe Rollen und Prioritäten an, wenn die Standardreihenfolge (Revenue → Team → Customers → Deep Work) nicht passt.

---

## Schritt 9: Skill in Kimi aufrufen

Sobald alles läuft, reicht in Kimi:

```
/chief-of-staff
```

Kimi liest den Skill, führt das Python-Modul aus und zeigt dir das Briefing.

---

## Schritt 10: Automatisieren

Wenn du mit dem Ergebnis zufrieden bist, kannst du das Briefing automatisch laufen lassen:

**Lokal mit `launchd` (macOS):**

Erstelle eine Datei `~/Library/LaunchAgents/ch.hartmut.chiefofstaff.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ch.hartmut.chiefofstaff</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/hartmut/Documents/ai-chief-of-staff/.venv/bin/python</string>
        <string>-m</string>
        <string>chief_of_staff</string>
        <string>run</string>
        <string>--preview</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/hartmut/Documents/ai-chief-of-staff</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/hartmut/Documents/ai-chief-of-staff/memory/history/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/hartmut/Documents/ai-chief-of-staff/memory/history/launchd.error.log</string>
</dict>
</plist>
```

Lade den Agent:

```bash
launchctl load ~/Library/LaunchAgents/ch.hartmut.chiefofstaff.plist
```

> Passe den Pfad `/Users/hartmut/...` an deinen tatsächlichen Benutzernamen an.

**Cloud mit GitHub Actions:**

Aktiviere den Workflow `.github/workflows/daily-briefing.yml` und hinterlege die Werte aus `.env` als Repository-Secrets.

---

## Nächste Schritte

- Quellen schrittweise erweitern (Slack, Telegram, Notion-Auslieferung).
- Approval-Dial in `config/chief_of_staff.toml` von `draft` auf `ask` oder `auto` setzen, sobald du dem Output vertraust.
- `memory/preferences.md` regelmäßig aktualisieren, damit der Chief of Staff dazulernt.

---

*Bei Problemen: Siehe [docs/mcp-setup.md](mcp-setup.md) und [docs/setup.md](setup.md).*
