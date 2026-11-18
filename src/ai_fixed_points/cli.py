"""Command-line interface for ai-fixed-points.

The ``ai-fixed-points`` command runs the iterative improvement loop over a
source file.  It wraps :func:`ai_fixed_points.improve_loop.multi_improve` into
a reproducible, scriptable CLI.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from .improve_loop import multi_improve

EX_OK = 0
EX_NOINPUT = 66


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the ``ai-fixed-points`` command."""
    parser = argparse.ArgumentParser(
        prog="ai-fixed-points",
        description=(
            "Iteratively improve a piece of code toward a fixed point using an "
            "LLM-driven agent."
        ),
    )
    parser.add_argument(
        "target",
        nargs="?",
        type=Path,
        help="Path to the source file to improve (defaults to base.py).",
    )
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=3,
        metavar="N",
        help="Maximum number of improvement rounds (default: 3).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=3.0,
        metavar="SECONDS",
        help="Delay between rounds, to respect rate limits (default: 3.0).",
    )
    parser.add_argument(
        "--profile",
        type=str,
        default=None,
        help="Config profile to use (overrides PSEUDO_SECTIONS_PROFILE).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point: parse arguments, run the loop, print the result."""
    parser = build_parser()
    args = parser.parse_args(argv)

    target = Path(__file__).with_name("base.py") if args.target is None else args.target

    if not target.is_file():
        parser.error(f"target file not found: {target}")

    code = target.read_text(encoding="utf-8")

    # The profile is consumed by BaseAgent via load_config(); pass it through
    # the environment so the agent picks it up without API changes.
    if args.profile is not None:
        import os

        os.environ["PSEUDO_SECTIONS_PROFILE"] = args.profile

    result = asyncio.run(
        multi_improve(user_input=code, max_round=args.max_rounds, delay=args.delay)
    )
    print(result)
    return EX_OK


if __name__ == "__main__":  # pragma: no cover - exercised via the entry point
    sys.exit(main())
