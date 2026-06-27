#!/usr/bin/env python3
"""Main orchestrator entry point for the personal AI chief-of-staff."""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import toml
from dotenv import load_dotenv


def get_project_root() -> Path:
    """Resolve project root from this script's location."""
    return Path(__file__).resolve().parents[4]


def ensure_dirs(root: Path) -> None:
    (root / "memory" / "source-cache").mkdir(parents=True, exist_ok=True)
    (root / "memory" / "output").mkdir(parents=True, exist_ok=True)


def load_config(root: Path) -> dict:
    config_path = root / "config" / "chief_of_staff.toml"
    if not config_path.exists():
        print(f"ERROR: config not found at {config_path}", file=sys.stderr)
        sys.exit(1)
    return toml.load(config_path)


def fetch_source(source: str, config: dict) -> dict:
    module_name = f"connectors.{source}"
    try:
        module = __import__(module_name, fromlist=[f"fetch_{source}"])
        fetch_fn = getattr(module, f"fetch_{source}")
        return fetch_fn(config)
    except Exception as exc:
        return {
            "source": source,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "error": str(exc),
            "items": [],
        }


def write_cache(root: Path, source: str, data: dict) -> Path:
    path = root / "memory" / "source-cache" / f"{source}.json"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the chief-of-staff daily briefing.")
    parser.add_argument(
        "--channel",
        choices=["console", "email", "slack", "notion"],
        help="Delivery channel (if omitted, preview mode is used).",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Skip interactive approval prompts.",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        default=True,
        help="Preview the briefing on stdout (default).",
    )
    args = parser.parse_args()

    root = get_project_root()
    env_path = root / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    config = load_config(root)
    ensure_dirs(root)

    enabled = config.get("sources", {}).get("enabled", [])
    if not enabled:
        print("ERROR: no sources enabled in config.", file=sys.stderr)
        sys.exit(1)

    cache_files = []
    for source in enabled:
        print(f"Fetching {source}...", file=sys.stderr)
        data = fetch_source(source, config)
        cache_path = write_cache(root, source, data)
        cache_files.append(cache_path.name)

    from synthesize import synthesize

    briefing_path, summary_path = synthesize(config, root)

    from deliver import deliver

    preview = args.preview if not args.channel else False
    delivery_result = deliver(
        root, channel=args.channel, preview=preview, auto_run=args.auto
    )

    run_summary = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "sources": enabled,
        "cache_files": cache_files,
        "briefing_path": str(briefing_path),
        "summary_path": str(summary_path),
        "delivery": delivery_result,
    }
    print(json.dumps(run_summary, indent=2))


if __name__ == "__main__":
    main()
