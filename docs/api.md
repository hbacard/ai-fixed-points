# API Reference

This page documents the public API of `ai_fixed_points`, version 0.1.0. All
paths are relative to the `src/ai_fixed_points/` package.

## Package overview

```
ai_fixed_points
├── __init__.py    # re-exports public symbols and __version__
├── base.py        # BaseAgent — model wiring, prompt loading, tracing
├── config.py      # Config / Profile / JudgeConfig, load_config()
├── improver.py    # CodeImprover — concrete code-improving agent
├── improve_loop.py# multi_improve() — iterative improvement loop
└── cli.py         # ai-fixed-points command line interface
```

## Top-level exports

| Symbol | Kind | Description |
|---|---|---|
| `__version__` | `str` | Installed package version (`0.1.0`). |
| `BaseAgent` | class | Base agent: wires an OpenAI-compatible model, loads the system prompt, and builds a Pydantic-AI agent. |
| `CodeImprover` | class | Concrete agent that improves code as a highly skilled engineer. |
| `Config` | class | Resolved runtime configuration. |
| `Profile` | class | A deployment profile: model + OpenAI-compatible base URL + API key env var. |
| `load_config` | function | Load configuration from `.env` and YAML profiles. |

```python
from ai_fixed_points import BaseAgent, CodeImprover, Config, Profile, __version__
from ai_fixed_points.config import load_config

cfg = load_config("openai")
print(__version__, cfg.profile.model)
```

## Configuration API

### `load_config(profile=None) -> Config`

Loads secrets from `.env` (via python-dotenv) and model profiles from
`config.yaml`, falling back to `config.yaml.example` when the local file is
absent.

**Profile resolution order:**

1. explicit `profile` argument
2. `DEFAULT_PROFILE` environment variable
3. `default_profile` key in the config file

**Raises:**

- `ValueError` — unknown profile, or profile missing required keys.
- `FileNotFoundError` — no config file found.

```python
from ai_fixed_points.config import load_config

cfg = load_config("ollama")  # explicit profile
cfg = load_config()  # env var or default_profile
```

### `Config`

A frozen dataclass with:

- `profile: Profile` — the selected deployment profile.
- `api_key: str | None` — the resolved API key, or `None`.
- `judge: JudgeConfig | None` — the judge configuration, or `None` (defaults to
  difflib string similarity).

### `Profile`

A frozen dataclass with:

- `name: str`
- `base_url: str` — the OpenAI-compatible base URL.
- `model: str`
- `api_var_env: str` — name of the env var (or `.env` key) holding the API key.

## Agent API

### `BaseAgent`

The base class for all agents. Subclasses set two class attributes and
optionally override `run`/`run_sync`.

**Required class attributes**

- `prompt_file: ClassVar[str]` — filename in `prompts/` that holds the system
  prompt (e.g. `"improve.md"`).
- `output_type: ClassVar[type]` — a Pydantic model type, or `str` (default).

**Constructor**

```python
BaseAgent(config: Config | None = None)
```

When `config` is `None`, the agent loads configuration via `load_config()`.

**Methods**

- `async run(user_input: str) -> Any` — run the agent asynchronously, wrapped
  in a Langfuse observation that traces input and output.
- `run_sync(user_input: str) -> Any` — synchronous counterpart of `run()`.

```python
from ai_fixed_points.base import BaseAgent


class Reviewer(BaseAgent):
    """Review code and return a structured verdict."""

    prompt_file = "review.md"
    output_type = str  # or a Pydantic model
```

### `CodeImprover`

`BaseAgent` subclass that improves code. Uses `prompt_file = "improve.md"` and
`output_type = str`.

```python
from ai_fixed_points.improver import CodeImprover
import asyncio

agent = CodeImprover()
out = asyncio.run(agent.run("def add(a,b):\n    return a-b\n"))
print(out)
```

## Improvement loop API

### `async multi_improve(user_input, max_round=3, delay=3.0) -> str`

Applies the `CodeImprover` agent repeatedly, feeding each round's output back
in as the next input, until a *fixed point* is reached or `max_round` is hit.

**Parameters**

- `user_input: str` — initial code to improve.
- `max_round: int = 3` — maximum number of improvement rounds.
- `delay: float = 3.0` — seconds to wait between rounds (rate limiting).

**Returns**

- `str` — final result of the last round.

```python
import asyncio
from ai_fixed_points.improve_loop import multi_improve

code = open("my_file.py").read()
result = asyncio.run(multi_improve(user_input=code, max_round=3, delay=1.0))
print(result)
```

## CLI

### `ai-fixed-points`

Runs the improvement loop over a source file from the command line.

```bash
ai-fixed-points path/to/source.py --max-rounds 5 --delay 1.0
ai-fixed-points --max-rounds 3          # defaults to src/ai_fixed_points/base.py
```

| Option | Default | Description |
|---|---|---|
| `target` (positional) | `base.py` | Path to the source file to improve. |
| `--max-rounds` | `3` | Maximum number of improvement rounds. |
| `--delay` | `3.0` | Delay between rounds, in seconds. |
| `--profile` | `None` | Config profile to use. |

Exit code is `0` on success, or `66` (`EX_NOINPUT`) if the target file is
missing.
