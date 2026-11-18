# Software Sustainability Plan

**Project**: ai-fixed-points
**Maintainer**: Hugo Bacard (**IJCLab**, hugo.bacard@ijclab.in2p3.fr)
**Version**: 0.1.0 — 2026-11-18

This plan describes how ai-fixed-points stays maintainable, funded, and usable
over the long term. It follows the RSQKit guidance on
[software maintenance](https://everse.software/RSQKit/software_maintenance).

## 1. Governance and maintenance

- **Ownership**: single maintainer (Hugo Bacard), with contribution guidelines
  in `CONTRIBUTING.md` and a code of conduct in `CODE_OF_CONDUCT.md`.
- **Versioning**: semantic versioning (`X.Y.Z`) with tagged releases and a
  `CHANGELOG.md`; see `RELEASING` notes in `CONTRIBUTING.md`.
- **Code review**: all changes land via pull requests (template + CODEOWNERS),
  reviewed before merge.
- **Automated quality gates**: CI runs lint, format check, and tests on every
  PR; static analysis via ruff; dependency updates via Dependabot.

## 2. Funding and institutional support

- **Host institution**: developed under the umbrella of **IJCLab** (Laboratoire
  de Physique des 2 Infinis Irène Joliot-Curie, CNRS/Université Paris-Saclay).
- **Open-source model**: Apache-2.0 licensed; contributions welcome from the
  community. No commercial funding is required for current scope.
- **Sustainability principle**: keep maintenance effort low through automation
  (CI, Dependabot, lockfiles) so a single maintainer can sustain the project.

## 3. Dependencies and lockfiles

- Runtime dependencies are intentionally few (`pydantic-ai`, `python-dotenv`,
  `langfuse`) and pinned via `uv.lock` / `pdm.lock`.
- Dependabot opens PRs for dependency updates; CI validates each update.
- The ML-model dependency (OpenAI-compatible APIs) is external and decoupled
  through configurable profiles, so the tool does not break when a single
  provider changes.

## 4. Documentation and community

- End-user docs in `README.md` and a hosted manual via **MkDocs**
  (`docs/`, `mkdocs.yml`).
- API reference in `docs/api.md`.
- Easy onboarding: issue/PR templates, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`,
  and a reproducible dev environment.

## 5. Long-term preservation

- Source archived on **Zenodo** (DOI badge in README) at each release.
- Metadata kept current in `CITATION.cff`, `codemeta.json`, `.zenodo.json`.
- The repository is public on GitHub under an archive-friendly, permissive
  license (Apache-2.0), maximizing the chance others can reuse and continue it.

## 6. Risk register

| Risk | Mitigation |
|---|---|
| Maintainer leaves | Permissive license, full docs, CI automation, archive on Zenodo, open contribution model |
| Dependency abandonment | Small dependency set, lockfiles, Dependabot monitoring, LLM-provider-agnostic design |
| LLM providers change APIs | Providers abstracted behind OpenAI-compatible `base_url` profiles |
| Funding ends | Zero-cost hosting (GitHub Actions, GitHub Pages), no paid services required |

## 7. Review cadence

This plan is reviewed at every minor/major release and updated when the
project's scope, dependencies, or governance change.
