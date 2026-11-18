"""Tests for configuration loading and validation."""

from __future__ import annotations

import pytest
import yaml

from ai_fixed_points import config

SAMPLE = """\
default_profile: openai
profiles:
  openai:
    base_url: https://api.openai.com/v1
    model: gpt-4o-mini
    api_var_env: OPENAI_API_KEY
  ollama:
    base_url: http://localhost:11434/v1
    model: llama3.1
    api_var_env: OLLAMA_API_KEY
judge:
  mode: similarity
"""


@pytest.fixture
def config_file(tmp_path, monkeypatch):
    """Point config.CONFIG_FILE at an isolated temp file."""
    path = tmp_path / "config.yaml"
    path.write_text(SAMPLE, encoding="utf-8")
    monkeypatch.setattr(config, "CONFIG_FILE", path)
    return path


def test_config_yaml_example_is_committed_and_valid():
    path = config.CONFIG_EXAMPLE_FILE
    assert path.exists()
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert raw["default_profile"] == "openai"
    assert "openai" in raw["profiles"]


def test_load_config_uses_default_profile(config_file):
    cfg = config.load_config()
    assert cfg.profile.name == "openai"
    assert cfg.profile.base_url == "https://api.openai.com/v1"
    assert cfg.profile.model == "gpt-4o-mini"


def test_load_config_selects_explicit_profile(config_file):
    cfg = config.load_config(profile="ollama")
    assert cfg.profile.name == "ollama"
    assert cfg.profile.api_var_env == "OLLAMA_API_KEY"


def test_load_config_unknown_profile_raises(config_file):
    with pytest.raises(ValueError, match="Unknown profile"):
        config.load_config(profile="does-not-exist")


def test_load_config_invalid_judge_mode_raises(tmp_path, monkeypatch):
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        "default_profile: openai\n"
        "profiles:\n"
        "  openai:\n"
        "    base_url: https://api.openai.com/v1\n"
        "    model: gpt-4o-mini\n"
        "    api_var_env: OPENAI_API_KEY\n"
        "judge:\n"
        "  mode: nope\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(config, "CONFIG_FILE", bad)
    with pytest.raises(ValueError, match="Unknown judge mode"):
        config.load_config(profile="openai")


def test_load_config_judge_mode(config_file):
    cfg = config.load_config()
    assert cfg.judge is not None
    assert cfg.judge.mode == "similarity"


def test_api_key_read_from_environment(config_file, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    cfg = config.load_config()
    assert cfg.api_key == "test-key"
