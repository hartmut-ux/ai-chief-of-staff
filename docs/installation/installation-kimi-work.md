# Skill in Kimi Work installieren (macOS)

Diese Anleitung führt dich Schritt für Schritt durch die Installation eines Skills aus diesem Repo in Kimi Work. Du brauchst kein Terminal — alles läuft über den Finder.

**Geprüfter Speicherort für Skills in Kimi Work (macOS):**

```
~/Library/Application Support/kimi-desktop/daimon-share/daimon/skills/<skill-name>/SKILL.md
```

Wichtig: Der Ordnername muss dem Skill-Namen entsprechen, und die Datei `SKILL.md` liegt direkt in diesem Ordner — nicht in einem Unterordner wie `kimi/`.

## Schritt 1: ZIP herunterladen

1. Öffne das Repo auf GitHub.
2. Klicke auf den grünen Button **Code** und dann auf **Download ZIP**.
3. Alternativ: Lade das ZIP eines Releases herunter, falls eines angeboten wird.

## Schritt 2: ZIP entpacken

1. Öffne den Ordner **Downloads** im Finder.
2. Doppelklicke die ZIP-Datei. macOS entpackt sie in einen Ordner mit dem Repo-Namen.

## Schritt 3: Den richtigen Skill-Ordner finden

Im entpackten Ordner liegt jeder Skill dreifach — einmal pro Umgebung:

```
skills/<skill-name>/kimi/SKILL.md
skills/<skill-name>/claude/SKILL.md
skills/<skill-name>/codex/SKILL.md
```

Für Kimi Work brauchst du den Ordner **`kimi`** innerhalb deines Wunsch-Skills. Er ist vollständig eigenständig — du musst nichts weiter aus dem Repo mitnehmen.

## Schritt 4: Ordner an den Skills-Speicherort kopieren

1. Öffne ein neues Finder-Fenster.
2. Drücke **Umschalt + Cmd + G** («Gehe zum Ordner») und gib diesen Pfad ein:

   ```
   ~/Library/Application Support/kimi-desktop/daimon-share/daimon/skills
   ```

   Falls der Ordner `skills` noch nicht existiert, lege ihn an: In der Finder-Ansicht des übergeordneten Ordners (`daimon`) mit **Cmd + Umschalt + N** einen neuen Ordner erstellen und `skills` nennen.

3. Ziehe den Ordner `kimi` aus dem entpackten Repo in den `skills`-Ordner.
4. Benenne den kopierten Ordner um — aus `kimi` wird der Skill-Name, zum Beispiel `sokratischer-fall-interviewer`. Das Ergebnis sieht so aus:

   ```
   ~/Library/Application Support/kimi-desktop/daimon-share/daimon/skills/sokratischer-fall-interviewer/SKILL.md
   ```

5. Wiederhole Schritt 3 und 4 für jeden weiteren Skill, den du installieren willst.

## Schritt 5: Kimi Work neu starten

Beende Kimi Work vollständig (**Cmd + Q**) und starte die App neu. Erst dann lädt Kimi Work neue Skills aus dem Ordner.

## Schritt 6: Skill aufrufen

Sprich den Skill im Chat mit seinem Namen an, zum Beispiel:

> Interviewe mich mit dem Skill «sokratischer-fall-interviewer» zu meinem Fall.

Wenn der Skill nicht reagiert: Prüfe, ob der Ordnername exakt stimmt und ob die Datei `SKILL.md` direkt im Ordner liegt — nicht eine Ebene zu tief.

## Häufige Stolpersteine

- **Ordner eine Ebene zu tief:** Beim Entpacken entsteht manchmal eine verschachtelte Struktur. Die `SKILL.md` muss direkt unter `skills/<skill-name>/` liegen.
- **Falsche Umgebung kopiert:** Für Kimi Work immer den Ordner `kimi` nehmen, nicht `claude` oder `codex`.
- **App nicht neu gestartet:** Ein Fenster schliessen reicht nicht — die App muss vollständig beendet und neu geöffnet werden.
