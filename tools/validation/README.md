# tools/validation/

Repository validation implementation scripts used by the canonical wrapper entrypoint:

- `../../scripts/validate-repo-structure.sh`
- `validate-repo-structure.sh`

`validate-repo-structure.sh` is the canonical repository-validation implementation and is expected to run in both:
- normal git checkouts
- extracted zip review environments (with explicit degraded-mode messaging where git-only checks are unavailable)
