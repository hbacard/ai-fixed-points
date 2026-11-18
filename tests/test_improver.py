"""Tests for the CodeImprover agent wiring."""

from __future__ import annotations

from ai_fixed_points.base import BaseAgent
from ai_fixed_points.improver import CodeImprover


def test_improver_subclasses_base_agent():
    assert issubclass(CodeImprover, BaseAgent)


def test_improver_uses_improve_prompt():
    assert CodeImprover.prompt_file == "improve.md"


def test_improver_output_type_is_str():
    assert CodeImprover.output_type is str
