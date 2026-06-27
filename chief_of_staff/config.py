"""Configuration and environment loading."""

from pathlib import Path
from typing import Any

import toml
from dotenv import load_dotenv

from . import get_project_root


def load_env(root: Path | None = None) -> None:
    """Load .env file from the project root if it exists."""
    if root is None:
        root = get_project_root()
    env_path = root / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=False)


def load_config(root: Path | None = None) -> dict[str, Any]:
    """Load chief_of_staff.toml from the project config directory."""
    if root is None:
        root = get_project_root()
    config_path = root / "config" / "chief_of_staff.toml"
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found at {config_path}")
    return toml.load(config_path)


def ensure_dirs(root: Path | None = None) -> Path:
    """Ensure runtime memory directories exist."""
    if root is None:
        root = get_project_root()
    (root / "memory" / "source-cache").mkdir(parents=True, exist_ok=True)
    (root / "memory" / "output").mkdir(parents=True, exist_ok=True)
    return root
