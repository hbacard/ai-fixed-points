# ai-fixed-points

An LLM-driven **code improvement agent** that repeatedly rewrites a piece of
code toward a *fixed point* — a state the model no longer meaningfully changes.
Each round feeds the previous output back into the agent, producing
progressively cleaner, safer code.

Built on [Pydantic AI](https://ai.pydantic.dev/) with OpenAI-compatible models,
fully traceable through [Langfuse](https://langfuse.com/).


## Features

- **Configurable LLM profiles** — OpenAI, Ollama, or any OpenAI-compatible base
  URL (`api.openai.com`, `localhost:11434/v1`, …).
- **Iterative improvement loop** — `multi_improve()` applies the agent several
  rounds, with a configurable delay between rounds to respect rate limits.
- **Pluggable judge** — `llm` (LLM-as-a-judge) or `similarity` (difflib string
  similarity) modes.
- **Secret-safe configuration** — API keys come from a gitignored `.env` file;
  machine-specific settings from a gitignored `config.yaml`.
- **Tracing** — every agent round is recorded in Langfuse for observability.

## Installation

The project is managed with [uv](https://docs.astral.sh/uv/) (or
[PDM](https://pdm-project.org/)). Either lockfile is provided.

```bash
# Clone the repository
git clone https://github.com/hbacard/ai-fixed-points.git
cd ai-fixed-points

# With uv
uv sync --extra dev

# Or with PDM
pdm install --dev
```

Create a virtual environment if you prefer managing it by hand:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Configuration

1. **Secrets** (`.env`, gitignored): create a `.env` from the template and set
   your provider keys.

   ```dotenv
   OPENAI_API_KEY=sk-...
   ```

2. **Model settings** (`config.yaml`, gitignored): copy
   `config.yaml.example` and adjust the profiles.

   ```bash
   cp config.yaml.example config.yaml
   ```

   When `config.yaml` is absent, the tool falls back to the committed
   `config.yaml.example` template, so it stays importable in a fresh checkout
   or CI. Profiles are resolved in this order: explicit `profile` argument →
   `PSEUDO_SECTIONS_PROFILE` env var → `default_profile` key.

## Usage

The quickest way to see it in action:

```bash
uv run python -m ai_fixed_points.improve_loop
```

or via the installed CLI:

```bash
ai-fixed-points path/to/source.py --max-rounds 3
```

or, from within the package:

```python
import asyncio
from ai_fixed_points.improve_loop import multi_improve

code = open("my_file.py").read()
result = asyncio.run(multi_improve(user_input=code, max_round=3))
print(result)
```

### Running with Docker

A multi-stage `Dockerfile` is provided for reproducible deployment:

```bash
# Build and run the CLI inside a container
docker build -t ai-fixed-points .
docker run --rm ai-fixed-points
docker run --rm -v "$PWD/src:/work" ai-fixed-points /work/ai_fixed_points/base.py
```

Secrets are passed through the environment (`-e OPENAI_API_KEY=...`); local
`config.yaml`/`.env` are **not** baked into the image.

### Writing a custom agent

Subclass `BaseAgent`, point `prompt_file` at a prompt in `prompts/`, and define
an `output_type`:

```python
from ai_fixed_points.base import BaseAgent


class Reviewer(BaseAgent):
    """Review code and return a structured verdict."""

    prompt_file = "review.md"
    output_type = str  # or a Pydantic model
```

## Project structure

```
.
├── src/ai_fixed_points/   # source package
│   ├── base.py            # BaseAgent: model wiring, prompt loading, tracing
│   ├── config.py          # config loading (.env + config.yaml profiles)
│   ├── improver.py        # CodeImprover: concrete code-improving agent
│   ├── improve_loop.py    # multi_round iterative improvement loop
│   └── cli.py             # ai-fixed-points command line entry point
├── prompts/               # system prompts for agents
├── tests/                 # pytest suite
├── docs/                  # documentation (MkDocs site; see mkdocs.yml)
├── Dockerfile             # reproducible container image
├── config.yaml.example    # committed config template
└── pyproject.toml
```

## Documentation & project documents

- `docs/api.md` — full API reference (also served as an MkDocs site).
- [REPRODUCIBILITY.md](REPRODUCIBILITY.md) — how to reproduce results.
- [DMP.md](DMP.md) — data management plan.
- [SUSTAINABILITY.md](SUSTAINABILITY.md) — software sustainability plan.
- [SECURITY.md](SECURITY.md) — how to report vulnerabilities.
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute.

## Testing

```bash
uv run pytest            # or: pdm run pytest
uv run ruff check .      # lint
uv run ruff format .     # format
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of
conduct and the process for submitting pull requests.

## License

Distributed under the [Apache License 2.0](LICENSE). See `LICENSE` for more
information. Copyright © 2026 Hugo Bacard.
