"""Command-line interface for chief_of_staff."""

import argparse
import json
from pathlib import Path

from . import get_project_root
from .config import load_config, load_env
from .delivery import CHANNELS, deliver
from .runner import run
from .synthesis import synthesize


def build_parser() -> argparse.ArgumentParser:
    """Build the argparse parser."""
    parser = argparse.ArgumentParser(
        prog="chief_of_staff",
        description="AI-agnostic personal chief of staff.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser(
        "run",
        help="Run the full GATHER → SYNTHESIZE → DELIVER workflow.",
    )
    run_parser.add_argument(
        "--preview",
        action="store_true",
        default=True,
        help="Preview the briefing on stdout (default).",
    )
    run_parser.add_argument(
        "--channel",
        choices=list(CHANNELS.keys()),
        help="Delivery channel.",
    )
    run_parser.add_argument(
        "--auto",
        action="store_true",
        dest="auto_run",
        help="Skip interactive approval prompts.",
    )

    subparsers.add_parser(
        "synthesize",
        help="Synthesize cached sources into a briefing.",
    )

    deliver_parser = subparsers.add_parser(
        "deliver",
        help="Deliver the generated briefing.",
    )
    deliver_parser.add_argument(
        "--preview",
        action="store_true",
        default=True,
        help="Preview the briefing on stdout (default).",
    )
    deliver_parser.add_argument(
        "--channel",
        choices=list(CHANNELS.keys()),
        help="Delivery channel.",
    )
    deliver_parser.add_argument(
        "--auto",
        action="store_true",
        dest="auto_run",
        help="Skip interactive approval prompts.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    root = get_project_root()
    load_env(root)

    if args.command == "run":
        preview = args.preview if not args.channel else False
        result = run(channel=args.channel, preview=preview, auto_run=args.auto_run)
        print(json.dumps(result, indent=2))
    elif args.command == "synthesize":
        config = load_config(root)
        briefing_path, summary_path = synthesize(config, root)
        print(f"Briefing written to {briefing_path}")
        print(f"Summary written to {summary_path}")
    elif args.command == "deliver":
        preview = args.preview if not args.channel else False
        result = deliver(
            channel=args.channel,
            preview=preview,
            auto_run=args.auto_run,
            root=root,
        )
        print(json.dumps(result, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
