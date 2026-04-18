# Validation Baseline

This repository keeps a lightweight, implementation-agnostic validation floor.

## Local validation

Run:

```bash
bash scripts/dev/validate.sh
```

The script validates:

- required scaffold paths and area README files
- markdown file sanity (non-empty and heading-first)
- shell script syntax under `scripts/`

## CI validation

Workflow: `.github/workflows/validation-baseline.yml`

- triggers on pull requests and pushes to `main`
- executes the same script used locally

## Future extension point

When tooling stacks are added (language/runtime-specific checks), keep this baseline script as the common floor and add tool-specific checks/jobs on top.
