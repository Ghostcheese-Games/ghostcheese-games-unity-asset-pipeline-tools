# UI Toolkit Graphics Package Validator

This document describes the first production tool slice in this repository: validating Unity UI Toolkit graphic asset packages against the shared manifest/schema foundation and package structure expectations.

## Validator entrypoint

- `tools/pipeline/ui_toolkit_graphics/validate_package.py`

## What this validator checks

Shared foundation alignment:

- required top-level foundation fields exist (`manifestSchemaVersion`, `manifestKind`, `common`, `pipeline`)
- `manifestSchemaVersion` and `manifestKind` match shared foundation constants
- required `common` fields exist and key fields follow expected formats (`manifestId`, governance scope, source, assets)
- required `pipeline` fields exist and `familySchemaVersion` is semver
- `pipeline.family` is specifically `ui-toolkit-graphics`
- `pipeline.payload` is a non-empty object

Package structure and file integrity:

- package root contains `manifest.json` (or alternate `--manifest-name`)
- `common.assets[].path` values are safe relative paths and files exist under package root
- `pipeline.payload.visualTreeAssets[]` is present and non-empty
- `visualTreeAssets[]` entries are safe relative `.uxml` paths, exist, and are listed in `common.assets`
- optional `styleSheets[]` entries are safe relative `.uss` paths, exist, and are listed in `common.assets`

## Local usage

Validate one package:

```bash
python3 tools/pipeline/ui_toolkit_graphics/validate_package.py \
  --package-root /absolute/or/relative/path/to/package-root
```

The command prints human-readable validation messages and exits with:

- `0` when validation passes
- non-zero when validation fails (CI-friendly)

Run repository validation baseline (includes validator integration tests):

```bash
./tools/validation/validate-repo-structure.sh
```

## Fixtures and integration tests

- fixtures: `fixtures/validation/ui-toolkit-graphics-package/`
- test matrix: `tests/integration/ui-toolkit-graphics-package-validator/cases.json`
- test runner: `tests/integration/ui-toolkit-graphics-package-validator/test_validator.py`

## Intended usage by game repos and production handoff workflows

In game repositories or production handoff automation, use thin wrappers that call this shared validator and pass game-local package roots/config.

This preserves the shared-governed validation logic in this repository and aligns with the documented game-repo consumption model.
