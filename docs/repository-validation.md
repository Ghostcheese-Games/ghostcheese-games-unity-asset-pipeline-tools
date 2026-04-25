# Repository Validation

This repository keeps a lightweight, implementation-agnostic validation floor.

## Local validation

Run:

```bash
./tools/validation/validate-repo-structure.sh
```

The script validates:

- required scaffold paths and area README files
- markdown file sanity (non-empty and heading-first)
- shell script syntax under `tools/validation/` and `tools/release/`
- UI Toolkit graphics package validator integration cases

Implementation note:

- `tools/validation/validate-repo-structure.sh` is the canonical validation entrypoint

## CI validation

Workflow: `.github/workflows/repository-validation.yml`

- triggers on pull requests and pushes to `main`
- executes the same script used locally

## Future extension point

When tooling stacks are added (language/runtime-specific checks), keep this baseline script as the common floor and add tool-specific checks/jobs on top.
