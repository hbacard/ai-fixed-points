"""Tests for the ``ai-fixed-points`` command line entry point."""

from __future__ import annotations

import os

import pytest

from ai_fixed_points.cli import EX_NOINPUT, EX_OK, build_parser, main
from ai_fixed_points.improve_loop import multi_improve


def test_build_parser_defaults():
    parser = build_parser()
    args = parser.parse_args([])
    assert args.max_rounds == 3
    assert args.delay == 3.0
    assert args.profile is None
    assert args.target is None


def test_main_default_target_no_network(monkeypatch, capsys):
    # main() must not require the LLM when the loop never runs a round.
    async def fake_multi_improve(user_input, max_round, delay):
        return user_input

    # cli.main() refers to the module-level import in the cli namespace.
    monkeypatch.setattr(
        "ai_fixed_points.cli.multi_improve",
        fake_multi_improve,
    )
    rc = main(["--max-rounds", "0"])
    captured = capsys.readouterr()
    assert rc == EX_OK
    assert captured.out != ""


def test_main_with_explicit_target(tmp_path, monkeypatch, capsys):
    source = tmp_path / "sample.py"
    source.write_text("def f():\n    return 1\n", encoding="utf-8")

    async def fake_multi_improve(user_input, max_round, delay):
        return "improved"

    monkeypatch.setattr("ai_fixed_points.cli.multi_improve", fake_multi_improve)
    rc = main([str(source), "--max-rounds", "2", "--delay", "0.5"])
    captured = capsys.readouterr()
    assert rc == EX_OK
    assert "improved" in captured.out


def test_main_default_target_is_base_py(monkeypatch, capsys):
    async def fake_multi_improve(user_input, max_round, delay):
        return f"len={len(user_input)}"

    monkeypatch.setattr("ai_fixed_points.cli.multi_improve", fake_multi_improve)
    rc = main(["--max-rounds", "1"])
    captured = capsys.readouterr()
    assert rc == EX_OK
    assert captured.out.startswith("len=") and int(captured.out.split("=")[1]) > 0


def test_main_missing_target_errors(tmp_path, capsys):
    with pytest.raises(SystemExit) as exc_info:
        main([str(tmp_path / "does_not_exist.py")])
    assert exc_info.value.code == 2
    assert "not found" in capsys.readouterr().err


def test_main_profile_env_is_set_and_cleaned(tmp_path, monkeypatch):
    source = tmp_path / "sample.py"
    source.write_text("def f():\n    return 1\n", encoding="utf-8")

    calls = {}

    async def fake_multi_improve(user_input, max_round, delay):
        calls["profile"] = os.environ.get("DEFAULT_PROFILE")
        return user_input

    monkeypatch.setattr("ai_fixed_points.cli.multi_improve", fake_multi_improve)
    monkeypatch.setenv("DEFAULT_PROFILE", "sentinel")

    # Explicit, non-empty --profile overrides any pre-set env var.
    rc = main([str(source), "--profile", "ollama", "--max-rounds", "0"])
    assert rc == EX_OK
    assert calls.get("profile") == "ollama"


def test_main_uses_preexisting_profile_env(tmp_path, monkeypatch):
    source = tmp_path / "sample.py"
    source.write_text("def f():\n    return 1\n", encoding="utf-8")

    calls = {}

    async def fake_multi_improve(user_input, max_round, delay):
        calls["profile"] = os.environ.get("DEFAULT_PROFILE")
        return user_input

    monkeypatch.setattr("ai_fixed_points.cli.multi_improve", fake_multi_improve)
    monkeypatch.setenv("DEFAULT_PROFILE", "ollama")

    # No --profile: the existing env var is left untouched.
    rc = main([str(source), "--max-rounds", "0"])
    assert rc == EX_OK
    assert calls.get("profile") == "ollama"


def test_exit_codes_defined():
    assert EX_OK == 0
    assert EX_NOINPUT == 66


def test_multi_improve_is_importable_from_cli_module():
    import ai_fixed_points.cli as cli_module

    assert cli_module.multi_improve is multi_improve
