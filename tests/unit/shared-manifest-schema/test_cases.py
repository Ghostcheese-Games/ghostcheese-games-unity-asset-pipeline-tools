#!/usr/bin/env python3
"""Validate shared-manifest schema fixtures against expected pass/fail outcomes."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _validate_required(
    payload: dict[str, Any], required_fields: list[str], instance_path: str
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    for field in required_fields:
        if field not in payload:
            errors.append(
                {
                    "instancePath": instance_path,
                    "keyword": "required",
                    "missingProperty": field,
                }
            )
    return errors


def _validate_enum(value: Any, enum_values: list[Any], instance_path: str) -> list[dict[str, str]]:
    if value is None:
        return []
    if value not in enum_values:
        return [{"instancePath": instance_path, "keyword": "enum"}]
    return []


def _validate_manifest(manifest: dict[str, Any], schema: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    errors.extend(_validate_required(manifest, schema.get("required", []), ""))

    common = manifest.get("common")
    if isinstance(common, dict):
        common_required = schema.get("$defs", {}).get("commonManifest", {}).get("required", [])
        errors.extend(_validate_required(common, common_required, "/common"))

    pipeline = manifest.get("pipeline")
    if isinstance(pipeline, dict):
        family_enum = (
            schema.get("$defs", {})
            .get("pipelineExtensionPoint", {})
            .get("properties", {})
            .get("family", {})
            .get("enum", [])
        )
        errors.extend(_validate_enum(pipeline.get("family"), family_enum, "/pipeline/family"))

    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parents[3]
    cases_path = repo_root / "tests" / "unit" / "shared-manifest-schema" / "cases.json"
    with cases_path.open("r", encoding="utf-8") as handle:
        spec = json.load(handle)

    schema = _load_json(repo_root / spec["schema"])

    failures: list[str] = []
    for case in spec["cases"]:
        fixture_path = repo_root / case["fixture"]
        fixture_payload = _load_json(fixture_path)
        if not isinstance(fixture_payload, dict):
            failures.append(f"{case['name']}: fixture must be a JSON object: {fixture_path}")
            continue

        errors = _validate_manifest(fixture_payload, schema)
        is_valid = len(errors) == 0
        if is_valid != case["expectValid"]:
            failures.append(
                f"{case['name']}: expected valid={case['expectValid']}, got valid={is_valid}. errors={errors!r}"
            )
            continue

        expected_failure = case.get("expectedFailure")
        if expected_failure is not None:
            if not any(
                all(error.get(key) == value for key, value in expected_failure.items()) for error in errors
            ):
                failures.append(
                    f"{case['name']}: expected failure fragment {expected_failure!r} not found in errors={errors!r}"
                )

    if failures:
        print("Shared-manifest schema fixture tests failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Shared-manifest schema fixture tests passed ({len(spec['cases'])}/{len(spec['cases'])} cases).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
