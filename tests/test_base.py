"""Tests for the base agent: prompt loading and package metadata."""

from __future__ import annotations

import ai_fixed_points as afp
from ai_fixed_points import config as config_module
from ai_fixed_points.base import BaseAgent


class _DummyAgent(BaseAgent):
    prompt_file = "improve.md"
    output_type = str


def test_prompts_dir_contains_improve_prompt():
    prompt_path = config_module.PROMPTS_DIR / "improve.md"
    assert prompt_path.exists()
    assert len(prompt_path.read_text(encoding="utf-8")) > 0


def test_load_prompt_reads_prompt_file():
    agent = object.__new__(_DummyAgent)
    prompt = agent._load_prompt()
    assert "world-class software engineer" in prompt


def test_load_prompt_uses_class_prompt_file():
    agent = object.__new__(_DummyAgent)
    assert agent._load_prompt().startswith("# Code Improver Agent")


def test_package_exports_and_version():
    assert afp.__version__ == "0.1.0"
    assert "BaseAgent" in afp.__all__
    assert "CodeImprover" in afp.__all__
