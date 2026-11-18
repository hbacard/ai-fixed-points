# Contributing to ai-fixed-points

Thanks for taking the time to contribute! We follow the
[Contributor Covenant](CODE_OF_CONDUCT.md), and we expect all participants to
adhere to it.

## How can I contribute?

### Reporting bugs / requesting features

Open an issue using the provided
[templates](.github/ISSUE_TEMPLATE/). Before filing, search to see if the
problem or request was already reported.

### Setting up a development environment

```bash
# With uv
uv sync --extra dev

# Or with PDM
pdm install --dev
```

### Making changes

1. Create a feature branch from `main`:

   ```bash
   git checkout -b feat/my-change main
   ```

2. Make your changes and add tests for them in `tests/`.
3. Run the checks locally:

   ```bash
   uv run ruff format .      # formatting
   uv run ruff check .       # linting
   uv run pytest             # tests (with coverage)
   ```

4. Commit with a clear message, following
   [Conventional Commits](https://www.conventionalcommits.org/):

   ```text
   feat(config): add support for custom base URLs
   fix(improve_loop): avoid blocking the event loop between rounds
   ```

5. Push the branch and open a pull request against `main` using the
   [pull request template](.github/pull_request_template.md).

### Code review

Every pull request must be reviewed by at least one maintainer (see
[CODEOWNERS](.github/CODEOWNERS)) before it can be merged. Be responsive to
review feedback and keep the discussion constructive.

## Style guide

- Code is formatted with [`ruff format`](https://docs.astral.sh/ruff/).
- Linting rules run under [`ruff check`](https://docs.astral.sh/ruff/) with the
  configuration in `pyproject.toml`.
- Docstrings follow the project's existing style; prefer code that reads
  clearly over comments that restate it.

## Releasing

Releases follow [Semantic Versioning](https://semver.org/). Maintainers create
a version tag (e.g. `v0.2.0`) and update `CHANGELOG.md`.
