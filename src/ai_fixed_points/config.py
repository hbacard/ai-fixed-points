"""Configuration loading.

Secrets (per-provider API keys, e.g. ``OPENAI_API_KEY``) come from a ``.env``
file via python-dotenv. Model settings and deployment profiles come from
``config.yaml``, falling back to the ``config.yaml.example`` template when no
local config exists.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_FILE = PROJECT_ROOT / "config.yaml"
CONFIG_EXAMPLE_FILE = PROJECT_ROOT / "config.yaml.example"
ENV_FILE = PROJECT_ROOT / ".env"
PROMPTS_DIR = PROJECT_ROOT / "prompts"

_PROFILE_ENV = "DEFAULT_PROFILE"


def _resolve_config_file() -> Path:
    """Return the active configuration file.

    Prefer the local ``config.yaml`` (gitignored, machine-specific); when it is
    absent — e.g. in a fresh checkout or CI — fall back to the committed
    ``config.yaml.example`` template.
    """
    if CONFIG_FILE.exists():
        return CONFIG_FILE
    if CONFIG_EXAMPLE_FILE.exists():
        return CONFIG_EXAMPLE_FILE
    raise FileNotFoundError(
        f"No config file found. Create {CONFIG_FILE} "
        f"(see the template at {CONFIG_EXAMPLE_FILE})."
    )


CONFIG_FILE = _resolve_config_file()


@dataclass(frozen=True)
class Profile:
    """A deployment profile: model + OpenAI-compatible base URL.

    ``api_var_env`` is the name of the environment variable (or ``.env`` key)
    holding the API key for this provider, e.g. ``OPENAI_API_KEY``.
    """

    name: str
    base_url: str
    model: str
    api_var_env: str


@dataclass(frozen=True)
class JudgeConfig:
    """Configuration for the adversarial-loop judge.

    ``mode`` is either ``"llm"`` (LLM-as-a-judge) or ``"similarity"`` (difflib
    string similarity). When ``profile`` is ``None`` the judge reuses the active
    configuration — profile and API key — so no duplicate setup happens; this is
    the default when ``judge.profile`` is omitted or set to ``default_profile``.
    """

    mode: str
    profile: Profile | None
    api_key: str | None


@dataclass(frozen=True)
class Config:
    """Resolved runtime configuration."""

    profile: Profile
    api_key: str | None
    judge: JudgeConfig | None = None


def _resolve_judge(raw: object, profiles: dict[str, object]) -> JudgeConfig | None:
    """Parse the top-level ``judge:`` block into a :class:`JudgeConfig`.

    Returns ``None`` when no ``judge`` key is present (the judge then defaults
    to string similarity). Otherwise ``mode`` defaults to ``"llm"`` and
    ``profile`` to ``default_profile`` — i.e. reusing the active profile.
    """
    judge_raw = raw.get("judge") if isinstance(raw, dict) else None
    if judge_raw is None:
        return None
    if not isinstance(judge_raw, dict):
        raise ValueError("'judge' must be a mapping with 'mode' and/or 'profile'.")

    mode = judge_raw.get("mode", "llm")
    if mode not in ("llm", "similarity"):
        raise ValueError(f"Unknown judge mode {mode!r}. Use 'llm' or 'similarity'.")

    profile_name = judge_raw.get("profile")
    if profile_name in (None, "", "default_profile"):
        # Reuse the active profile — no separate provider setup.
        return JudgeConfig(mode=mode, profile=None, api_key=None)

    if profile_name not in profiles:
        available = ", ".join(profiles) or "(none)"
        raise ValueError(
            f"Unknown judge profile {profile_name!r}. Available: {available}"
        )

    p = profiles[profile_name]
    missing = [k for k in ("base_url", "model", "api_var_env") if k not in p]
    if missing:
        raise ValueError(
            f"Judge profile {profile_name!r} is missing keys: {', '.join(missing)}"
        )

    return JudgeConfig(
        mode=mode,
        profile=Profile(
            name=profile_name,
            base_url=p["base_url"],
            model=p["model"],
            api_var_env=p["api_var_env"],
        ),
        api_key=os.environ.get(p["api_var_env"]),
    )


def load_config(profile: str | None = None) -> Config:
    """Load configuration from ``.env`` (secrets) and a YAML profiles file.

    Profiles come from ``config.yaml`` when present, otherwise from the
    ``config.yaml.example`` template.

    Profile resolution order:
      1. explicit ``profile`` argument
      2. ``DEFAULT_PROFILE`` environment variable
      3. ``default_profile`` key in the config file
    """
    load_dotenv(ENV_FILE)

    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")

    raw = yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8")) or {}
    profiles = raw.get("profiles", {})

    selected = profile or os.environ.get(_PROFILE_ENV) or raw.get("default_profile")
    if not selected:
        raise ValueError(
            "No profile selected. Pass a profile, set "
            f"{_PROFILE_ENV}, or define 'default_profile' in config.yaml."
        )
    if selected not in profiles:
        available = ", ".join(profiles) or "(none)"
        raise ValueError(f"Unknown profile {selected!r}. Available: {available}")

    p = profiles[selected]
    missing = [k for k in ("base_url", "model", "api_var_env") if k not in p]
    if missing:
        raise ValueError(f"Profile {selected!r} is missing keys: {', '.join(missing)}")

    api_key = os.environ.get(p["api_var_env"])

    return Config(
        profile=Profile(
            name=selected,
            base_url=p["base_url"],
            model=p["model"],
            api_var_env=p["api_var_env"],
        ),
        api_key=api_key,
        judge=_resolve_judge(raw, profiles),
    )
