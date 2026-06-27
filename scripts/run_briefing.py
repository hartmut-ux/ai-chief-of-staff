#!/usr/bin/env python3
"""Thin backward-compatible wrapper around the chief_of_staff CLI."""

import sys
from pathlib import Path

# Ensure the package is importable when this script is run directly.
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from chief_of_staff.cli import main


if __name__ == "__main__":
    # Prepend the "run" subcommand so old invocations keep working.
    sys.argv = ["chief_of_staff", "run"] + sys.argv[1:]
    raise SystemExit(main())
