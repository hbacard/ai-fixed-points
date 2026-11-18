"""Tests for the multi-round improvement loop."""

from __future__ import annotations

import asyncio
import inspect

from ai_fixed_points.improve_loop import multi_improve


def test_multi_improve_is_coroutine_function():
    assert inspect.iscoroutinefunction(multi_improve)


def test_multi_improve_default_max_rounds():
    sig = inspect.signature(multi_improve)
    assert sig.parameters["max_round"].default == 3


def test_multi_improve_zero_rounds_returns_input_unchanged():
    # With max_round=0 the agent is constructed but never invoked, so no
    # network access happens.
    source = "def f():\n    return 1\n"
    result = asyncio.run(multi_improve(source, max_round=0))
    assert result == source
