# ghostcheese-games-unity-asset-pipeline-tools

Shared, reusable tooling for Ghostcheese Games Unity asset pipelines.

This repository is the central home for cross-game asset-pipeline tooling infrastructure (validation, schema support, extraction/export/import helpers, package handoff support, and related automation). It is not a game repository and it is not the shared Unity runtime library repository.

## Repository status

Bootstrap scaffold complete; implementation work can now begin.

## Governance alignment

This repository follows governance in `Ghostcheese-Games/.github`, including:

- shared asset-pipeline tooling governance
- game-repo asset-pipeline tool consumption governance
- shared asset-pipeline tooling bootstrap governance
- localization-aware asset pipeline governance
- org-wide AI/agent workflow standards

Primary references:

- `https://github.com/Ghostcheese-Games/.github/blob/main/docs/governance/shared-asset-pipeline-tooling-governance.md`
- `https://github.com/Ghostcheese-Games/.github/blob/main/docs/governance/game-repo-asset-pipeline-tool-consumption-governance.md`
- `https://github.com/Ghostcheese-Games/.github/blob/main/docs/checklists/new-shared-asset-pipeline-tooling-repo-checklist.md`
- `https://github.com/Ghostcheese-Games/.github/blob/main/docs/governance/unity-localization-governance.md`
- `https://github.com/Ghostcheese-Games/.github/blob/main/.github/ai/AI-COLLABORATION-STANDARD.md`
- `https://github.com/Ghostcheese-Games/.github/blob/main/.github/ai/ISSUE-EXECUTION-STANDARD.md`

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
- `scripts/` — development and release automation scripts

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

This foundation separates strict `common` shared manifest concepts from `pipeline` extension payloads so future family-specific validators can evolve independently.

## Development notes

This scaffold is implementation-agnostic so the repo can host tooling in different languages over time.

Current state:

- no production tooling implementation yet
- no language-specific build/test stack configured yet

## Validation baseline

This repo includes a lightweight validation baseline that is intentionally implementation-agnostic.

Run locally:

```bash
bash scripts/dev/validate.sh
```

Current baseline checks:

- expected scaffold directories/files are present
- required area `README.md` files exist
- markdown files are non-empty and start with a heading
- shell scripts under `scripts/` are syntax-checked with `bash -n`

CI:

- GitHub Actions workflow: `.github/workflows/validation-baseline.yml`
- runs on pull requests and pushes to `main`
- executes the same local baseline script

Future tool-specific validation should plug in by extending `scripts/dev/validate.sh` and, if needed, adding toolchain-specific jobs/workflows while keeping this baseline as the common floor.
