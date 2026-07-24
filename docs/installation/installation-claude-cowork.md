# Skill in Claude Cowork / Claude Code installieren

Diese Anleitung zeigt dir die dokumentierten Wege, einen Skill aus diesem Repo in den Claude-Umgebungen von Anthropic zu installieren. Du brauchst kein Terminal.

Zuerst eine wichtige Unterscheidung, denn «Claude» hat mehrere Umgebungen mit unterschiedlichen Installationswegen:

- **Claude Cowork** (Desktop-App, Wissensarbeit mit eigenen Dateien)
- **Claude Code** (Terminal/IDE-Agent für Entwicklerinnen und Entwickler)
- **claude.ai** (Web-App)

## Weg 1: Skill über die Oberfläche hochladen (Cowork und claude.ai)

Dies ist der Weg für dich als CEO ohne Terminal — belegt durch die offizielle Anthropic-Hilfe ([How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills), [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)):

1. **ZIP herunterladen:** Öffne das Repo auf GitHub, klicke auf **Code → Download ZIP** und entpacke die Datei per Doppelklick.
2. **Skill-Ordner vorbereiten:** Nimm aus dem entpackten Repo den Ordner `claude` deines Wunsch-Skills (`skills/<skill-name>/claude/`). Benenne ihn in den Skill-Namen um, zum Beispiel `sokratischer-fall-interviewer`. Der Ordnername muss dem Skill-Namen entsprechen.
3. **Ordner zippen:** Rechtsklick auf den Ordner → **Komprimieren**. Das ZIP muss den Skill-Ordner als Wurzel enthalten, nicht als Unterordner eines anderen Ordners.
4. **Hochladen:** In der Claude-Desktop-App über **Customize** in der Seitenleiste — dort kannst du eigene Skills hinzufügen. Alternativ über die Skill-Einstellungen auf claude.ai.
5. **Aufrufen:** Sprich den Skill im Chat mit seinem Namen an.

⚠ zu verifizieren: Der exakte Klickpfad innerhalb von «Customize» (Menübenennung, ob «Add skill» oder «Upload») kann sich je nach App-Version unterscheiden. Beim Workshop prüfen wir das live an der aktuellen Version.

**Wichtig für Cowork:** Laut offizieller Doku ([Claude Code Docs — Skills](https://code.claude.com/docs/en/skills)) lesen Cowork-Sitzungen **nicht** den lokalen Ordner `~/.claude/skills/` auf deinem Rechner. Cowork lädt die Skills, die für dein claude.ai-Konto aktiviert sind — verwaltet über **Customize** in der Desktop-App oder die Skill-Einstellungen auf claude.ai. Der Upload über die Oberfläche ist also der richtige Weg für Cowork.

## Weg 2: Skill-Ordner direkt ablegen (Claude Code)

Falls du oder dein Team mit Claude Code arbeiten, ist der Weg aus der offiziellen Doku belegt ([Claude Code Docs — Skills](https://code.claude.com/docs/en/skills)):

| Ebene | Speicherort | Gilt für |
|---|---|---|
| Persönlich | `~/.claude/skills/<skill-name>/SKILL.md` | Alle deine Projekte |
| Projekt | `.claude/skills/<skill-name>/SKILL.md` | Nur dieses Projekt |

Vorgehen ohne Terminal:

1. ZIP des Repos herunterladen und entpacken.
2. Im Finder **Umschalt + Cmd + G** drücken und `~/.claude/skills` eingeben. Falls der Ordner nicht existiert, lege ihn an (`~/.claude` öffnen, neuen Ordner `skills` erstellen).
3. Den Ordner `claude` deines Wunsch-Skills hineinkopieren und in den Skill-Namen umbenennen. Ergebnis: `~/.claude/skills/sokratischer-fall-interviewer/SKILL.md`.
4. Claude Code erkennt neue und geänderte Skills laut Doku automatisch («live change detection») — ein Neustart ist nur nötig, wenn der übergeordnete Skills-Ordner neu angelegt wurde.
5. Aufruf im Chat per `/skill-name`, zum Beispiel `/sokratischer-fall-interviewer` — oder Claude lädt den Skill automatisch, wenn die Anfrage zur Beschreibung passt.

## Häufige Stolpersteine

- **In Cowork einen lokalen Ordner erwarten:** Cowork ignoriert `~/.claude/skills/` — hier zählt nur der Upload über Customize/claude.ai.
- **ZIP falsch gebaut:** Das ZIP muss den Skill-Ordner selbst als Wurzel enthalten. Wenn du den übergeordneten Ordner zippst, schlägt die Installation fehl.
- **Ordnername ≠ Skill-Name:** Der Ordnername muss exakt dem Skill-Namen entsprechen.

## Quellen

- [How to create custom skills — Anthropic Help Center](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Use skills in Claude — Anthropic Help Center](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
- [Extend Claude with skills — Claude Code Docs](https://code.claude.com/docs/en/skills)
