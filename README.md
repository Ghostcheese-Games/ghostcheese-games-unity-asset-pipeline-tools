# ghostcheese-games-unity-asset-pipeline-tools

Shared, reusable tooling for Ghostcheese Games Unity asset pipelines.

This repository is the central home for cross-game asset-pipeline tooling infrastructure (validation, schema support, extraction/export/import helpers, package handoff support, and related automation). It is not a game repository and it is not the shared Unity runtime library repository.

## Repository status

Bootstrap scaffold complete, with the first production validator slice implemented; broader implementation work continues.

## Governance alignment

This repository follows governance in `Ghostcheese-Games/.github`, including:

- shared asset-pipeline tooling governance
- game-repo asset-pipeline tool consumption governance
- shared asset-pipeline tooling bootstrap governance
- localization-aware asset pipeline governance
- org-wide AI/agent workflow standards
- centralized reusable pattern governance/indexing

Primary references:

- `https://github.com/Ghostcheese-Games/.github/blob/main/docs/governance/shared-asset-pipeline-tooling-governance.md`
- `https://github.com/Ghostcheese-Games/.github/blob/main/docs/governance/game-repo-asset-pipeline-tool-consumption-governance.md`
- `https://github.com/Ghostcheese-Games/.github/blob/main/docs/checklists/new-shared-asset-pipeline-tooling-repo-checklist.md`
- `https://github.com/Ghostcheese-Games/.github/blob/main/docs/governance/unity-localization-governance.md`
- `https://github.com/Ghostcheese-Games/.github/blob/main/.github/ai/AI-COLLABORATION-STANDARD.md`
- `https://github.com/Ghostcheese-Games/.github/blob/main/.github/ai/ISSUE-EXECUTION-STANDARD.md`
- `https://github.com/Ghostcheese-Games/.github/blob/main/docs/patterns/index.md`

Local pattern reference layer for this repository: `docs/patterns/README.md`.

## Scope and boundaries

What belongs here:

- reusable tooling used by more than one game repo
- shared schemas and contracts used by tooling
- shared validation/import/export helpers
- cross-repo examples and deterministic fixtures
- shared test harnesses for tooling behavior

What does not belong here:

- game runtime assets/content
- game-specific production pipelines and release evidence
- copied shared-tool source in game repos

See `docs/repo-scope-and-boundaries.md`.

## Consumption model for game repositories

Game repositories consume this tooling by release/version (tagged versions), not by copying tool source. Game repos may keep only project-specific configuration and thin wrappers.

See `docs/game-repo-consumption-model.md`.

## Top-level structure

- `docs/` — repo documentation and policy-aligned guidance
- `tools/` — reusable tool implementations and entrypoints
- `schemas/` — canonical schema definitions
- `examples/` — reference usage for consumers
- `fixtures/` — deterministic sample inputs/outputs for tests
- `tests/` — unit and integration test suites
- `scripts/` — release preparation automation scripts (optional; absent in minimal environments)
- `tools/validation/` — repo-validation implementation (canonical entrypoint)

## Supported pipeline domains

- UI Toolkit graphics
- 2D sprites
- 3D models
- textures/materials
- animation
- sound effects
- music
- voice-over
- VFX / particle / screen effects
- font / localized text-presentation

See `docs/supported-pipelines.md`.

## Shared manifest/schema foundation

The initial shared manifest/schema foundation is defined for cross-pipeline tooling adoption:

- schema: `schemas/pipeline/shared-manifest.foundation.schema.json`
- design doc: `docs/shared-manifest-schema-foundation.md`
- examples: `examples/pipeline-packages/shared-manifest.*.example.json`
- validation fixtures: `fixtures/validation/shared-manifest/`

## First real tool slice: UI Toolkit graphics package validator

This repository now includes a first end-to-end validator slice for Unity UI Toolkit graphic asset packages:

- validator entrypoint: `tools/pipeline/ui_toolkit_graphics/validate_package.py`
- integration test matrix: `tests/integration/ui-toolkit-graphics-package-validator/cases.json`
- package fixtures: `fixtures/validation/ui-toolkit-graphics-package/`

Python requirement: Python 3.10+.

Run directly:

```bash
python3 tools/pipeline/ui_toolkit_graphics/validate_package.py \
  --package-root fixtures/validation/ui-toolkit-graphics-package/valid/minimal-package
```

Run repository validation (includes validator integration tests):

```bash
./tools/validation/validate-repo-structure.sh
```

This foundation separates strict `common` shared manifest concepts from `pipeline` extension payloads so future family-specific validators can evolve independently.

## Development notes

This scaffold is implementation-agnostic so the repo can host tooling in different languages over time.

Current state:

- first production tooling implementation exists (UI Toolkit graphics package validator)
- no additional language-specific build/test stack configured yet beyond Python-based validator integration

## Validation baseline

This repo includes a lightweight validation baseline that is intentionally implementation-agnostic.

Run locally:

```bash
./tools/validation/validate-repo-structure.sh
```

Current baseline checks:

- expected scaffold directories/files are present
- required area `README.md` files exist
- markdown files are non-empty and start with a heading
  - when git metadata is unavailable (for example extracted zip review), markdown checks fall back to filesystem discovery with an explicit degraded-mode message
- generated Python/tooling artifacts are not present in repository tree (`__pycache__/`, `*.pyc`, `.pytest_cache/`)
- shell scripts under `tools/validation/` are syntax-checked with `bash -n`
- shared-manifest/schema fixture matrix runs via `python3 tests/unit/shared-manifest-schema/test_cases.py`
- UI Toolkit graphics package validator integration matrix runs via `python3` (Python 3.10+)

CI:

- GitHub Actions workflow: `.github/workflows/repository-validation.yml`
- runs on pull requests and pushes to `main`
- executes the same local baseline script

`tools/validation/validate-repo-structure.sh` is the canonical validation entrypoint.

Future tool-specific validation should plug in by extending `tools/validation/validate-repo-structure.sh` and, if needed, adding toolchain-specific jobs/workflows while keeping this baseline entrypoint stable.
