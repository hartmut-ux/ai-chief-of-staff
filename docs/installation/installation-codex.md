# Skill in OpenAI Codex installieren

Diese Anleitung zeigt dir die dokumentierten Wege, einen Skill aus diesem Repo in Codex zu installieren. Belegt durch die offizielle OpenAI-Doku ([Codex — Skills](https://developers.openai.com/codex/skills)).

Zuerst die Einordnung: Codex-Skills funktionieren in der **ChatGPT-Desktop-App**, in der **Codex CLI** und in der **IDE-Erweiterung**. Ein Skill ist ein Ordner mit einer Datei `SKILL.md` — genau so liegen die Skills in diesem Repo vor.

## Wo Codex Skills sucht (offiziell dokumentiert)

| Ebene | Speicherort | Gilt für |
|---|---|---|
| Persönlich (USER) | `~/.agents/skills/<skill-name>/SKILL.md` | Alle deine Projekte — der richtige Ort für dich als CEO |
| Projekt (REPO) | `.agents/skills/` im Arbeitsordner | Nur dieses Projekt |
| System (ADMIN) | `/etc/codex/skills/` | Geräteweit, für Administration |

Codex erkennt neue und geänderte Skills laut Doku automatisch; falls ein Skill nicht auftaucht, starte Codex neu.

## Weg 1: Skill-Ordner direkt ablegen (ohne Terminal)

Das ist der empfohlene Weg für die Workshop-Skills:

1. **ZIP herunterladen:** Öffne das Repo auf GitHub, klicke auf **Code → Download ZIP** und entpacke die Datei per Doppelklick.
2. **Zielordner öffnen:** Drücke im Finder **Umschalt + Cmd + G** und gib `~/.agents/skills` ein. Falls der Ordner nicht existiert, lege ihn an: `~/.agents` öffnen (oder erstellen) und darin einen neuen Ordner `skills` erstellen.
3. **Skill kopieren:** Nimm aus dem entpackten Repo den Ordner `codex` deines Wunsch-Skills (`skills/<skill-name>/codex/`), kopiere ihn nach `~/.agents/skills/` und benenne ihn in den Skill-Namen um. Ergebnis zum Beispiel:

   ```
   ~/.agents/skills/sokratischer-fall-interviewer/SKILL.md
   ```

4. **Aufrufen:** Tippe in Codex `$` gefolgt vom Skill-Namen (zum Beispiel `$sokratischer-fall-interviewer`) oder wähle den Skill über den Befehl `/skills`. Codex kann den Skill auch selbst aktivieren, wenn deine Anfrage zur Beschreibung passt.

## Weg 2: ChatGPT-Desktop-App

In der ChatGPT-Desktop-App gibt es laut Doku in der Seitenleiste den Bereich **Skills**, in dem du Skills aus deinen Projekten siehst und erkundest.

⚠ zu verifizieren: Ob und wie eigene Skills in der Desktop-App direkt per Upload installiert werden können, ist in der Doku nicht eindeutig beschrieben. Die Doku empfiehlt für die Verteilung an andere das Plugin-Format. Der sicher funktionierende Weg ist Weg 1 (Ordner ablegen) — den prüfen wir beim Workshop live.

## Weg 3: Eingebauter Installer (für kuratierte Skills)

Codex bringt den Skill `$skill-installer` mit, der kuratierte Skills aus offiziellen Quellen installiert. Er ist für fertige Drittanbieter-Skills gedacht, nicht für unsere Workshop-Skills — der Vollständigkeit halber erwähnt.

## Häufige Stolpersteine

- **Veraltete Pfad-Angaben im Netz:** Drittanbieter-Anleitungen nennen teils `~/.codex/skills/` als Speicherort. Die offizielle Doku nennt als persönlichen Ort `~/.agents/skills/`. Halte dich an die offizielle Angabe.
- **Falsche Umgebung kopiert:** Für Codex immer den Ordner `codex` nehmen, nicht `kimi` oder `claude`.
- **Ordnername ≠ Skill-Name:** Der Ordner muss so heissen wie der Skill, und `SKILL.md` muss direkt darin liegen.

## Quellen

- [Codex — Skills (offizielle OpenAI-Doku)](https://developers.openai.com/codex/skills)
- [Codex — Build skills (offizielle OpenAI-Doku)](https://developers.openai.com/codex/build-skills)
