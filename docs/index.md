# ai-fixed-points documentation

Welcome to the ai-fixed-points documentation.

- [README](https://github.com/hbacard/ai-fixed-points/blob/main/README.md) — overview, installation, configuration, and usage.
- [API Reference](api.md) — the full `ai_fixed_points` API and CLI.
- [DMP](https://github.com/hbacard/ai-fixed-points/blob/main/DMP.md) — data management plan.
- [REPRODUCIBILITY](https://github.com/hbacard/ai-fixed-points/blob/main/REPRODUCIBILITY.md) — how to reproduce results.
- [SUSTAINABILITY](https://github.com/hbacard/ai-fixed-points/blob/main/SUSTAINABILITY.md) — software sustainability plan.
- [CONTRIBUTING](https://github.com/hbacard/ai-fixed-points/blob/main/CONTRIBUTING.md) — how to contribute.
- [CODE_OF_CONDUCT](https://github.com/hbacard/ai-fixed-points/blob/main/CODE_OF_CONDUCT.md) — community standards.
- [SECURITY](https://github.com/hbacard/ai-fixed-points/blob/main/SECURITY.md) — how to report vulnerabilities.
- [CHANGELOG](https://github.com/hbacard/ai-fixed-points/blob/main/CHANGELOG.md) — release history.
- [LICENSE](https://github.com/hbacard/ai-fixed-points/blob/main/LICENSE) — the Apache-2.0 license.

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
| `src/ai_fixed_points/cli.py`      | `ai-fixed-points` command line entry point             |
| `prompts/improve.md`              | System prompt for the improving agent                   |

## Running tests

```bash
uv run pytest            # tests + coverage
uv run ruff check .      # lint
uv run ruff format .     # format
```
