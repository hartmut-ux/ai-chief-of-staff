"""Console delivery driver."""


def deliver(content: str, config: dict | None = None, auto_run: bool = False) -> dict:
    """Print the briefing to stdout."""
    print(content)
    return {"channel": "console", "status": "success", "note": "printed to stdout"}
