# Release and Versioning

This repository uses semantic versioning for reusable tooling releases.

## Versioning policy

- tags follow `v<MAJOR>.<MINOR>.<PATCH>`
- changes are tracked in root `CHANGELOG.md`
- breaking changes require explicit migration notes

## Consumer expectations

- game repos pin to released versions
- avoid floating references such as `main`, `master`, or `latest`
- upgrades should include validation of impacted pipelines

## Release notes scope

Each release should describe:

- schema/tooling changes
- compatibility implications
- migration or config updates required for consumers
