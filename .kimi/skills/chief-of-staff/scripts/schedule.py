#!/usr/bin/env python3
"""Print scheduling snippets for the daily briefing."""
import getpass
import sys
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[4]


def main() -> None:
    root = get_project_root()
    script = root / ".kimi" / "skills" / "chief-of-staff" / "scripts" / "run_briefing.py"
    python = sys.executable

    cron = f"""# Run the chief-of-staff daily briefing every morning at 07:00
0 7 * * * {python} {script} --channel console >> {root}/memory/output/cron.log 2>&1
"""

    plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.chiefofstaff.daily-briefing</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python}</string>
        <string>{script}</string>
        <string>--channel</string>
        <string>console</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>{root}/memory/output/launchctl.out.log</string>
    <key>StandardErrorPath</key>
    <string>{root}/memory/output/launchctl.err.log</string>
</dict>
</plist>
"""

    print("=== crontab snippet ===")
    print(cron)
    print("=== launchctl plist snippet ===")
    print(plist)
    print(
        f"Install plist:\n"
        f"  cp /tmp/ai.chiefofstaff.daily-briefing.plist ~/Library/LaunchAgents/\n"
        f"  launchctl load ~/Library/LaunchAgents/ai.chiefofstaff.daily-briefing.plist"
    )


if __name__ == "__main__":
    main()
