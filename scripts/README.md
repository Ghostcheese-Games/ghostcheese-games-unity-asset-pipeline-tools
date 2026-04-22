# scripts/

Automation scripts for development and release workflows.

- `validate-repo-structure.sh` canonical top-level validation baseline entrypoint (delegates to `../tools/validation/validate-repo-structure.sh`)
  - runs shared-manifest/schema unit fixture checks and UI Toolkit graphics validator integration checks
  - supports degraded filesystem-mode markdown discovery when `.git` metadata is unavailable (for extracted zip review)
- `release/` for release preparation automation
