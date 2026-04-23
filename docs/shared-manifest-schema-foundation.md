# Shared Manifest/Schema Foundation

This document defines the initial shared manifest/schema foundation for Ghostcheese Games asset-pipeline tooling.

## Goals of this first foundation

- establish one shared manifest contract for cross-game tooling
- separate common/shared concepts from pipeline-family extensions
- keep the foundation practical and incremental so validators/importers can adopt it quickly

## Canonical schema artifact

- `schemas/pipeline/shared-manifest.foundation.schema.json`

Schema version in this foundation:

- `manifestSchemaVersion: "1.0.0"`

## Shared/common manifest concepts

The `common` section is strictly defined and reusable across all pipeline families.

Core fields:

- `manifestId` — stable, machine-friendly manifest identifier
- `displayName` / `description` — human-readable metadata
- `governanceScope` — governance ownership model
- `source` — repository and relative source root for provenance
- `assets[]` — normalized asset entries used by shared tooling
- optional shared metadata (`tags`, `lifecycle`)

These fields are the shared contract for future generic validators/importers.

## Pipeline-specific extension point

The `pipeline` section is the extension boundary.

- `pipeline.family` identifies governed pipeline family
- `pipeline.familySchemaVersion` versions the family contract independently
- `pipeline.payload` carries family-specific fields

In this foundation, `pipeline.payload` is intentionally open for incremental adoption. Future issues can add family-specific schemas that validate `payload` per `family`.

## Example usage

- `examples/pipeline-packages/shared-manifest.ui-toolkit.example.json`
- `examples/pipeline-packages/shared-manifest.audio.example.json`

These examples show shared/common metadata plus different `pipeline.payload` shapes.

## Validation fixtures and test matrix

- Valid fixture:
  - `fixtures/validation/shared-manifest/valid/ui-toolkit.valid.json`
- Invalid fixtures:
  - `fixtures/validation/shared-manifest/invalid/missing-common.manifest-id.json`
  - `fixtures/validation/shared-manifest/invalid/unknown-family.json`
- Case matrix for validators:
  - `tests/unit/shared-manifest-schema/cases.json`

This gives future tooling issues deterministic fixtures and expected outcomes without requiring a specific implementation stack yet.
