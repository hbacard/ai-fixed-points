"""Run an improvement loop that iteratively improves a codebase.

Each round feeds the previous output back into the agent, so the code evolves
toward a *fixed point*: a state the model no longer meaningfully changes.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from .improver import CodeImprover


async def multi_improve(user_input: str, max_round: int = 3, delay: float = 3.0) -> str:
    """Improve ``user_input`` repeatedly and return the final result.

    Args:
        user_input: Initial code to improve.
        max_round: Maximum number of improvement rounds.
        delay: Seconds to wait between rounds, to respect rate limits.
    """
    current = user_input
    improver_agent = CodeImprover()
    for _ in range(max_round):
        current = await improver_agent.run(current)
        if _ < max_round - 1:
            await asyncio.sleep(delay)
    return current


if __name__ == "__main__":
    code_base = Path(__file__).with_name("base.py").read_text(encoding="utf-8")
    result = asyncio.run(multi_improve(user_input=code_base))
    print(result)
