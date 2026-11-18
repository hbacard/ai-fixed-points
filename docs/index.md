# ai-fixed-points documentation

Welcome to the ai-fixed-points documentation.

- [README](../README.md) — overview, installation, configuration, and usage.
- [CONTRIBUTING](../CONTRIBUTING.md) — how to contribute.
- [CODE_OF_CONDUCT](../CODE_OF_CONDUCT.md) — community standards.
- [SECURITY](../SECURITY.md) — how to report vulnerabilities.
- [CHANGELOG](../CHANGELOG.md) — release history.
- [LICENSE](../LICENSE) — the Apache-2.0 license.

## About

`ai-fixed-points` is an LLM-driven code improvement agent. Given a piece of
code, it repeatedly rewrites it — feeding each round's output back in — until
the code reaches a *fixed point*: a state the model no longer meaningfully
changes.

## Architecture

| Module                            | Responsibility                                          |
|-----------------------------------|---------------------------------------------------------|
| `src/ai_fixed_points/base.py`     | `BaseAgent`: model wiring, prompt loading, Langfuse tracing |
| `src/ai_fixed_points/config.py`   | Configuration loading (`.env` secrets + YAML profiles)  |
| `src/ai_fixed_points/improver.py` | `CodeImprover`: concrete code-improving agent           |
| `src/ai_fixed_points/improve_loop.py` | Iterative `multi_improve()` loop                    |
| `prompts/improve.md`              | System prompt for the improving agent                   |

## Running tests

```bash
uv run pytest            # tests + coverage
uv run ruff check .      # lint
uv run ruff format .     # format
```
