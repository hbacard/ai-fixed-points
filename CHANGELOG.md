# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-11-18

### Added

- Initial release: LLM-driven code improvement agent.
- `BaseAgent` (Pydantic AI wiring, OpenAI-compatible models, Langfuse tracing).
- `CodeImprover` concrete agent with a reusable improvement prompt (`prompts/improve.md`).
- Iterative `multi_improve()` loop that improves code toward a fixed point.
- Configurable profiles (`.env` secrets + `config.yaml` / `config.yaml.example`).
- Configurable judge modes: `llm` and `similarity`.
- Project hygiene: package layout, pytest suite, ruff, CI-ready metadata
  (README, LICENSE, CITATION.cff, codemeta.json, .zenodo.json).

[0.1.0]: https://github.com/hbacard/ai-fixed-points/releases/tag/v0.1.0
