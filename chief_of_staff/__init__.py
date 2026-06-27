"""AI-agnostic personal chief-of-staff package."""

from pathlib import Path

__version__ = "0.1.0"


def get_project_root() -> Path:
    """Resolve the project root as the parent of this package directory."""
    return Path(__file__).resolve().parents[1]
