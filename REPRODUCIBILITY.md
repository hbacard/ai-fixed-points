# Reproducibility Checklist

This checklist documents how to reproduce results with **ai-fixed-points**,
from a fresh machine to running the tool and the test suite, so that the
outcome is as deterministic and verifiable as possible.

- [ ] **Pin the environment** — the project declares `requires-python >=3.12,<3.14`
      and ships two lockfiles (`uv.lock`, `pdm.lock`) that pin every transitive
      dependency. Use one of the two to avoid version drift.
- [ ] **Use a clean virtual environment** — create one (`uv sync --extra dev` or
      `pdm install --dev`) and install the package in editable mode. Do **not**
      `pip install` dependencies ad hoc.
- [ ] **Set up local, gitignored config** — copy `config.yaml.example` to
      `config.yaml` and create a `.env` with your provider keys. Note that when
      `config.yaml` is absent, the tool falls back to the committed example —
      so the code stays importable in a fresh checkout.
- [ ] **Declare the model/profile** — record which profile (provider,
      `base_url`, `model`) you used. Result changes with the model and its
      version, so this must be part of any reported result.
- [ ] **Record the LLM/temperature settings** — if you customized judge mode
      (`llm` vs `similarity`), `max_round`, or `delay`, note them alongside the
      output.
- [ ] **Run the loop** — `ai-fixed-points path/to/source.py --max-rounds N` or
      `python -m ai_fixed_points.improve_loop`, and save the output.
- [ ] **Run the test suite** — `uv run pytest` (17 tests) and confirm the
      coverage gate passes (`fail_under = 70`).
- [ ] **Run static analysis** — `uv run ruff check .` and `uv run ruff format
      --check .` are clean, matching what CI enforces.
- [ ] **CI is deterministic** — GitHub Actions runs the same lint + test jobs on
      Python 3.12 and 3.13, so a green `main` is a strong reproducibility
      signal.

## Expected guarantees vs. caveats

- **Deterministic parts**: the test suite, lint/format checks, and the
  environment (lockfiles) are fully deterministic.
- **Non-deterministic parts**: LLM outputs are stochastic. The *quality* of the
  improvement is not byte-for-byte reproducible across model version or
  temperature changes — the checklist above is what makes it *verifiable*.

## Archiving

Tagged releases are archived on Zenodo (DOI badge in the README) to preserve
the exact source at each release point.

See [DMP.md](DMP.md) for how the underlying data is managed.
