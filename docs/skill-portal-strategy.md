# Strategie: Claude Skills für Kimi, Claude & Codex verfügbar machen

Diese Seite beschreibt die beste Vorgehensweise, um bestehende **Claude Skills** (bisher als ZIP-Dateien verteilt) in ein **Multi-Plattform-Skill-Portal** umzuwandeln, das unter **Kimi Code CLI**, **Claude Code** und **Codex CLI** funktioniert.

---

## Ausgangslage

- Du hast bereits mehrere Claude Skills als ZIP-Dateien.
- Jede ZIP enthält typischerweise `.claude/skills/<skill-name>/SKILL.md` und eventuell Ressourcen.
- Du möchtest diese Skills auch für Kimi- und Codex-Nutzer anbieten, ohne alles dreimal zu pflegen.

## Ziel

Ein separates Repository oder eine GitHub Page, auf der:

- Jeder Skill als **eine einzige Quelle** gepflegt wird.
- Pro Skill automatisch **plattformspezifische Wrapper** erzeugt werden.
- Besucher die Skills als ZIP für ihre Plattform herunterladen können.
- GitHub Releases die ZIP-Dateien hosten.

---

## Empfohlene Architektur

```text
skill-portal/
├── index.md                          # GitHub Pages Landing Page
├── README.md                         # Repo-Dokumentation
├── _config.yml                       # Jekyll / GitHub Pages Konfiguration
├── skills/
│   └── <skill-name>/
│       ├── README.md                 # Skill-Beschreibung
│       ├── shared/
│       │   └── SKILL-CORE.md         # Plattform-agnostischer Kern
│       ├── .kimi/skills/<skill-name>/SKILL.md
│       ├── .claude/skills/<skill-name>/SKILL.md
│       └── .codex/skills/<skill-name>/SKILL.md
├── scripts/
│   └── package-skill.py              # Baut ZIP-Dateien pro Skill
└── .github/workflows/
    └── release-skills.yml            # Erstellt bei jedem Release ZIP-Archive
```

### Plattform-agnostischer Kern

Der gemeinsame Inhalt jedes Skills liegt in `shared/SKILL-CORE.md`. Dort stehen:

- Zweck und Trigger des Skills
- Detaillierter Workflow
- Beispiel-Prompts
- Regeln und Grenzen
- Referenzen

### Thin Wrapper pro Plattform

Jede `SKILL.md` unter `.kimi/`, `.claude/` und `.codex/` ist ein dünner Wrapper, der:

1. Das Frontmatter mit Namen und kurzer Beschreibung enthält.
2. Verweist: "Lies `shared/SKILL-CORE.md` für den vollständigen Skill."
3. Plattformspezifische Aufrufe ergänzt (z. B. `/skill-name` bei Kimi, `skill-name` bei Claude/Codex).

So pflegst du den eigentlichen Skill nur einmal im `shared/`-Ordner.

---

## Vorgehen beim Migrieren einer bestehenden Claude Skill

1. **ZIP entpacken** und `SKILL.md` identifizieren.
2. **Kern extrahieren:** Kopiere den Inhalt von `.claude/skills/<name>/SKILL.md` nach `shared/SKILL-CORE.md`.
3. **Plattform-Referenzen neutralisieren:** Ersetze "Claude" durch "dein AI-Assistant" oder verwende pro Wrapper unterschiedliche Formulierungen.
4. **Wrapper erstellen:** Erzeuge die drei `SKILL.md`-Dateien mit jeweils passendem Frontmatter.
5. **Gemeinsame Assets auslagern:** Prompts, Templates, Code-Beispiele kommen in `shared/`.
6. **ZIP bauen:** Nutze `scripts/package-skill.py`, um pro Plattform und als Gesamtpaket ZIP-Dateien zu erzeugen.
7. **Release:** Lade die ZIPs als GitHub Release hoch oder hoste sie direkt auf GitHub Pages.

---

## Vorteile dieser Struktur

| Vorteil | Erklärung |
|---|---|
| **Single source of truth** | Skill-Logik liegt in `shared/SKILL-CORE.md`. |
| **Keine Code-Duplikation** | Wrapper sind dünn und verweisen auf den Kern. |
| **Einfache Wartung** | Änderungen am Skill erfordern nur eine Datei. |
| **Plattform-agnostisch** | Neue Plattformen lassen sich später mit einem weiteren Wrapper hinzufügen. |
| **Automatisierte Releases** | GitHub Actions baut ZIPs bei jedem Tag. |

---

## Download-Optionen für Nutzer

Auf der GitHub Page oder im README bietest du pro Skill folgende Downloads an:

- `example-skill-all.zip` — enthält alle drei Wrapper + shared (für Nutzer, die mehrere Assistenten nutzen)
- `example-skill-kimi.zip` — nur Kimi-Wrapper + shared
- `example-skill-claude.zip` — nur Claude-Wrapper + shared
- `example-skill-codex.zip` — nur Codex-Wrapper + shared

---

## Installation beim Nutzer

### Kimi Code CLI

```bash
# ZIP entpacken, dann den Ordner in Kimis Skill-Verzeichnis kopieren
cp -R .kimi/skills/example-skill ~/.kimi/skills/
# Aufruf in Kimi:
/example-skill
```

### Claude Code

```bash
# ZIP entpacken, dann den Ordner in Claudes Skill-Verzeichnis kopieren
cp -R .claude/skills/example-skill ~/.claude/skills/
# Aufruf in Claude:
skill-name
```

### Codex CLI

```bash
# ZIP entpacken, dann den Ordner in Codex' Skill-Verzeichnis kopieren
cp -R .codex/skills/example-skill ~/.codex/skills/
# Aufruf in Codex:
skill-name
```

---

## SEO / AI Search

Die GitHub Page sollte:

- Klare H1 mit Keywords enthalten: "AI Skills for Kimi, Claude & Codex".
- Pro Skill eine eigene Seite mit Beschreibung, Anwendungsfall und Installationsanleitung haben.
- FAQ-Sektionen enthalten, wie "How do I install a Kimi skill?" oder "Can I use the same skill in Claude and Codex?".
- Meta-Description im Frontmatter setzen.

---

## Fertiges Template

Ein vollständiges Template findest du im Ordner [`skill-portal/`](../skill-portal/) dieses Repos. Du kannst es als Grundlage für dein neues GitHub-Repository verwenden.
