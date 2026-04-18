# Repo Scope and Boundaries

## What belongs in this shared tooling repo

- reusable tooling logic expected to be consumed by more than one game repository
- canonical shared schemas and validation contracts
- shared CLI/automation entrypoints used for pipeline checks/import
- deterministic fixtures and examples for reusable tooling behavior

## What belongs in game repositories instead

- game runtime assets and game-specific content packages
- game-specific release evidence and title-specific release docs
- game-local config for path mapping and per-project thresholds/toggles
- thin wrapper scripts that invoke shared tooling with game-local config

## Non-goals for this repo

- hosting game-specific runtime systems
- acting as a copy-source for vendoring tooling into game repos
- replacing shared Unity runtime/package library responsibilities
