"""Orchestrate GATHER → SYNTHESIZE → DELIVER."""

import json
from datetime import datetime, timezone
from pathlib import Path

from . import get_project_root
from .config import ensure_dirs, load_config, load_env
from .connectors import FETCHERS
from .delivery import deliver
from .synthesis import synthesize


def write_cache(root: Path, source: str, data: dict) -> Path:
    """Write a source result to memory/source-cache/<source>.json."""
    path = root / "memory" / "source-cache" / f"{source}.json"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def gather_sources(config: dict, root: Path) -> list[Path]:
    """Fetch all enabled sources and cache their results."""
    enabled = config.get("sources", {}).get("enabled", [])
    cache_files: list[Path] = []
    for source in enabled:
        fetcher = FETCHERS.get(source)
        fetched_at = datetime.now(timezone.utc).isoformat()
        if fetcher is None:
            data = {
                "source": source,
                "fetched_at": fetched_at,
                "configured": False,
                "note": f"No fetcher implemented for source '{source}'.",
                "items": [],
            }
        else:
            try:
                data = fetcher(config)
            except Exception as exc:
                data = {
                    "source": source,
                    "fetched_at": fetched_at,
                    "error": str(exc),
                    "items": [],
                }
        cache_files.append(write_cache(root, source, data))
    return cache_files


def run(channel: str | None = None, preview: bool = True, auto_run: bool = False) -> dict:
    """Run the full chief-of-staff workflow."""
    root = get_project_root()
    load_env(root)
    config = load_config(root)
    ensure_dirs(root)

    enabled = config.get("sources", {}).get("enabled", [])
    if not enabled:
        raise ValueError("No sources enabled in config.")

    cache_files = gather_sources(config, root)
    briefing_path, summary_path = synthesize(config, root)

    delivery_result = deliver(
        channel=channel,
        preview=preview,
        auto_run=auto_run,
        config=config,
        root=root,
    )

    return {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "sources": enabled,
        "cache_files": [str(p) for p in cache_files],
        "briefing_path": str(briefing_path),
        "summary_path": str(summary_path),
        "delivery": delivery_result,
    }
