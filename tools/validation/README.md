# tools/validation/

Repository validation implementation. `validate-repo-structure.sh` is the canonical validation entrypoint.

`validate-repo-structure.sh` is expected to run in both:
- normal git checkouts
- extracted zip review environments (with explicit degraded-mode messaging where git-only checks are unavailable)
