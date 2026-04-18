# Game-Repo Consumption Model

Game repositories must consume shared asset-pipeline tooling by release/version reference.

## Required consumption rules

- consume by tagged release/version (or explicitly approved immutable commit SHA)
- do not copy shared tooling source into game repos
- keep pinned versions in committed, reviewable config/manifest files
- use game-local config plus thin wrappers only

## Thin wrapper guidance

Allowed in game repos:

- invoking shared tooling entrypoints
- passing game-local config and path mapping
- normalizing local CI command ergonomics

Not allowed in game repos:

- duplicating reusable validator/import rule logic
- creating parallel forks of shared tooling behavior

## Upgrade model

- upgrade between released versions
- review release notes/changelog before upgrading
- document old/new version and any required game-side config updates
