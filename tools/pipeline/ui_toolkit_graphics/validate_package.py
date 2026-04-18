#!/usr/bin/env python3
"""Validate Unity UI Toolkit graphic asset packages against shared foundation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


IDENTIFIER_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,127}$")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _is_safe_relative_path(path: str) -> bool:
    candidate = Path(path)
    return (
        path != ""
        and "\\" not in path
        and not candidate.is_absolute()
        and ".." not in candidate.parts
        and "~" not in path
    )


def _require_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _normalize_relative_path(path: str) -> str:
    return Path(path).as_posix()


def _validate_additional_properties(
    data: dict[str, Any], allowed_fields: set[str], field_label: str, errors: list[str]
) -> None:
    for key in data:
        if key not in allowed_fields:
            errors.append(f"{field_label} contains unsupported field: {key}.")


def _path_stays_within_package_root(package_root: Path, relative_path: str) -> tuple[bool, str | None]:
    try:
        resolved_root = package_root.resolve()
        resolved_candidate = (package_root / relative_path).resolve()
    except (OSError, RuntimeError):
        return False, "could not be resolved"

    try:
        resolved_candidate.relative_to(resolved_root)
    except ValueError:
        return False, "resolves outside package root"
    return True, None


def validate_package(package_root: Path, manifest_name: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    info: list[str] = []

    repo_root = Path(__file__).resolve().parents[3]
    schema_path = repo_root / "schemas" / "pipeline" / "shared-manifest.foundation.schema.json"
    try:
        schema = _load_json(schema_path)
    except OSError as exc:
        errors.append(f"Shared foundation schema could not be read: {schema_path} ({exc})")
        return errors, info
    except json.JSONDecodeError as exc:
        errors.append(f"Shared foundation schema is not valid JSON: {schema_path} ({exc})")
        return errors, info

    if not _require_non_empty_string(manifest_name):
        errors.append("manifest-name must be a non-empty string.")
        return errors, info
    if not _is_safe_relative_path(manifest_name):
        errors.append(f"manifest-name must be a safe relative path: {manifest_name!r}.")
        return errors, info
    if Path(manifest_name).name != manifest_name:
        errors.append("manifest-name must not contain directory components or path separators.")
        return errors, info

    within_root, reason = _path_stays_within_package_root(package_root, manifest_name)
    if not within_root:
        errors.append(f"manifest-name {reason}: {manifest_name!r}.")
        return errors, info

    manifest_path = package_root / manifest_name
    if not manifest_path.is_file():
        errors.append(f"Missing manifest file: {manifest_path}")
        return errors, info

    try:
        manifest = _load_json(manifest_path)
    except OSError as exc:
        errors.append(f"Manifest could not be read: {manifest_path} ({exc})")
        return errors, info
    except json.JSONDecodeError as exc:
        errors.append(f"Manifest is not valid JSON: {manifest_path} ({exc})")
        return errors, info

    if not isinstance(manifest, dict):
        errors.append("Manifest root must be a JSON object.")
        return errors, info

    top_required = schema.get("required", [])
    for field in top_required:
        if field not in manifest:
            errors.append(f"Missing required top-level field: {field}")
    _validate_additional_properties(
        manifest,
        set(schema.get("properties", {}).keys()),
        "manifest",
        errors,
    )

    expected_schema_version = schema.get("properties", {}).get("manifestSchemaVersion", {}).get("const")
    if manifest.get("manifestSchemaVersion") != expected_schema_version:
        errors.append(
            f"manifestSchemaVersion must equal {expected_schema_version!r}, got {manifest.get('manifestSchemaVersion')!r}."
        )

    expected_kind = schema.get("properties", {}).get("manifestKind", {}).get("const")
    if manifest.get("manifestKind") != expected_kind:
        errors.append(f"manifestKind must equal {expected_kind!r}, got {manifest.get('manifestKind')!r}.")

    common = manifest.get("common")
    if not isinstance(common, dict):
        errors.append("common must be an object.")
        common = {}
    common_schema = schema.get("$defs", {}).get("commonManifest", {})
    _validate_additional_properties(
        common,
        set(common_schema.get("properties", {}).keys()),
        "common",
        errors,
    )

    common_required = common_schema.get("required", [])
    for field in common_required:
        if field not in common:
            errors.append(f"common.{field} is required.")

    manifest_id = common.get("manifestId")
    if manifest_id is not None and not (isinstance(manifest_id, str) and IDENTIFIER_RE.fullmatch(manifest_id)):
        errors.append("common.manifestId must match shared identifier format.")

    if "displayName" in common and not _require_non_empty_string(common.get("displayName")):
        errors.append("common.displayName must be a non-empty string.")
    common_display_name_schema = common_schema.get("properties", {}).get("displayName", {})
    common_display_name = common.get("displayName")
    max_display_name_length = common_display_name_schema.get("maxLength")
    if (
        isinstance(common_display_name, str)
        and isinstance(max_display_name_length, int)
        and len(common_display_name) > max_display_name_length
    ):
        errors.append(f"common.displayName must be at most {max_display_name_length} characters.")

    scope = common.get("governanceScope")
    allowed_scopes = common_schema.get("properties", {}).get("governanceScope", {}).get("enum", [])
    if scope is not None and scope not in allowed_scopes:
        errors.append(f"common.governanceScope must be one of: {', '.join(allowed_scopes)}.")

    source = common.get("source")
    if not isinstance(source, dict):
        errors.append("common.source must be an object.")
        source = {}
    source_schema = common_schema.get("properties", {}).get("source", {})
    _validate_additional_properties(
        source,
        set(source_schema.get("properties", {}).keys()),
        "common.source",
        errors,
    )
    if not _require_non_empty_string(source.get("repository")):
        errors.append("common.source.repository must be a non-empty string.")
    if "revision" in source and not _require_non_empty_string(source.get("revision")):
        errors.append("common.source.revision must be a non-empty string when present.")
    if not _require_non_empty_string(source.get("relativeRoot")):
        errors.append("common.source.relativeRoot must be a non-empty string.")

    assets = common.get("assets")
    if not isinstance(assets, list) or len(assets) == 0:
        errors.append("common.assets must be a non-empty array.")
        assets = []

    asset_paths: set[str] = set()
    for idx, asset in enumerate(assets):
        if not isinstance(asset, dict):
            errors.append(f"common.assets[{idx}] must be an object.")
            continue
        asset_schema = common_schema.get("properties", {}).get("assets", {}).get("items", {}).get("$ref")
        asset_schema_name = asset_schema.removeprefix("#/$defs/") if isinstance(asset_schema, str) else None
        asset_entry_schema = schema.get("$defs", {}).get(asset_schema_name or "", {})
        _validate_additional_properties(
            asset,
            set(asset_entry_schema.get("properties", {}).keys()),
            f"common.assets[{idx}]",
            errors,
        )

        for required in ("assetId", "path", "kind"):
            if required not in asset:
                errors.append(f"common.assets[{idx}].{required} is required.")

        asset_id = asset.get("assetId")
        if asset_id is not None and not (isinstance(asset_id, str) and IDENTIFIER_RE.fullmatch(asset_id)):
            errors.append(f"common.assets[{idx}].assetId must match shared identifier format.")

        asset_path = asset.get("path")
        if asset_path is not None:
            path_is_valid = True
            if not _require_non_empty_string(asset_path):
                errors.append(f"common.assets[{idx}].path must be a non-empty string.")
                path_is_valid = False
            elif not _is_safe_relative_path(asset_path):
                errors.append(f"common.assets[{idx}].path must be a safe relative path: {asset_path!r}.")
                path_is_valid = False
            else:
                within_root, reason = _path_stays_within_package_root(package_root, asset_path)
                if not within_root:
                    errors.append(f"common.assets[{idx}].path {reason}: {asset_path!r}.")
                    path_is_valid = False

            if path_is_valid:
                normalized_asset_path = _normalize_relative_path(asset_path)
                asset_paths.add(normalized_asset_path)
                if not (package_root / normalized_asset_path).is_file():
                    errors.append(f"Asset file listed in common.assets is missing: {asset_path}")

        kind = asset.get("kind")
        if kind is not None and not _require_non_empty_string(kind):
            errors.append(f"common.assets[{idx}].kind must be a non-empty string.")

    pipeline = manifest.get("pipeline")
    if not isinstance(pipeline, dict):
        errors.append("pipeline must be an object.")
        pipeline = {}
    pipeline_schema = schema.get("$defs", {}).get("pipelineExtensionPoint", {})
    _validate_additional_properties(
        pipeline,
        set(pipeline_schema.get("properties", {}).keys()),
        "pipeline",
        errors,
    )

    pipeline_required = pipeline_schema.get("required", [])
    for field in pipeline_required:
        if field not in pipeline:
            errors.append(f"pipeline.{field} is required.")

    allowed_families = pipeline_schema.get("properties", {}).get("family", {}).get("enum", [])
    family = pipeline.get("family")
    if family is not None and family not in allowed_families:
        errors.append(f"pipeline.family must be one of: {', '.join(allowed_families)}.")
    if family != "ui-toolkit-graphics":
        errors.append(f"pipeline.family must be 'ui-toolkit-graphics' for this validator, got {family!r}.")

    family_schema_version = pipeline.get("familySchemaVersion")
    if family_schema_version is not None and not (
        isinstance(family_schema_version, str) and SEMVER_RE.fullmatch(family_schema_version)
    ):
        errors.append("pipeline.familySchemaVersion must be a semver string (x.y.z).")

    payload = pipeline.get("payload")
    if not isinstance(payload, dict) or len(payload) == 0:
        errors.append("pipeline.payload must be a non-empty object.")
        payload = {}

    visual_tree_assets = payload.get("visualTreeAssets")
    if not isinstance(visual_tree_assets, list) or len(visual_tree_assets) == 0:
        errors.append("pipeline.payload.visualTreeAssets must be a non-empty array.")
        visual_tree_assets = []

    for idx, path in enumerate(visual_tree_assets):
        if not _require_non_empty_string(path):
            errors.append(f"pipeline.payload.visualTreeAssets[{idx}] must be a non-empty string.")
            continue
        if not _is_safe_relative_path(path):
            errors.append(f"pipeline.payload.visualTreeAssets[{idx}] must be a safe relative path: {path!r}.")
            continue
        within_root, reason = _path_stays_within_package_root(package_root, path)
        if not within_root:
            errors.append(f"pipeline.payload.visualTreeAssets[{idx}] {reason}: {path!r}.")
            continue
        if not path.endswith(".uxml"):
            errors.append(f"pipeline.payload.visualTreeAssets[{idx}] must end with .uxml: {path!r}.")
        normalized_path = _normalize_relative_path(path)
        if normalized_path not in asset_paths:
            errors.append(f"pipeline.payload.visualTreeAssets[{idx}] must also be listed in common.assets: {path}")
        if not (package_root / normalized_path).is_file():
            errors.append(f"pipeline.payload.visualTreeAssets[{idx}] file is missing: {path}")

    style_sheets = payload.get("styleSheets")
    if style_sheets is not None:
        if not isinstance(style_sheets, list):
            errors.append("pipeline.payload.styleSheets must be an array when present.")
            style_sheets = []
        for idx, path in enumerate(style_sheets):
            if not _require_non_empty_string(path):
                errors.append(f"pipeline.payload.styleSheets[{idx}] must be a non-empty string.")
                continue
            if not _is_safe_relative_path(path):
                errors.append(f"pipeline.payload.styleSheets[{idx}] must be a safe relative path: {path!r}.")
                continue
            within_root, reason = _path_stays_within_package_root(package_root, path)
            if not within_root:
                errors.append(f"pipeline.payload.styleSheets[{idx}] {reason}: {path!r}.")
                continue
            if not path.endswith(".uss"):
                errors.append(f"pipeline.payload.styleSheets[{idx}] must end with .uss: {path!r}.")
            normalized_path = _normalize_relative_path(path)
            if normalized_path not in asset_paths:
                errors.append(f"pipeline.payload.styleSheets[{idx}] must also be listed in common.assets: {path}")
            if not (package_root / normalized_path).is_file():
                errors.append(f"pipeline.payload.styleSheets[{idx}] file is missing: {path}")

    if not errors:
        info.append(f"Validated package at {package_root}.")
        info.append(f"Manifest: {manifest_path.name}")
        info.append(f"Assets referenced: {len(asset_paths)}")
        info.append(f"UI Toolkit visualTreeAssets: {len(visual_tree_assets)}")
        if isinstance(style_sheets, list):
            info.append(f"UI Toolkit styleSheets: {len(style_sheets)}")

    return errors, info


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a Unity UI Toolkit graphic asset package against the shared manifest foundation."
    )
    parser.add_argument(
        "--package-root",
        required=True,
        help="Path to the package root directory that contains the manifest and referenced assets.",
    )
    parser.add_argument(
        "--manifest-name",
        default="manifest.json",
        help="Manifest file name within the package root. Default: manifest.json",
    )
    return parser.parse_args()


def main() -> int:
    if sys.version_info < (3, 10):
        print("Python 3.10+ is required.", file=sys.stderr)
        return 1

    args = parse_args()
    package_root = Path(args.package_root).resolve()

    if not package_root.is_dir():
        print(f"Validation failed: package root does not exist or is not a directory: {package_root}")
        return 1

    errors, info = validate_package(package_root=package_root, manifest_name=args.manifest_name)

    if errors:
        print(f"Validation failed for package: {package_root}")
        for error in errors:
            print(f"- ERROR: {error}")
        return 1

    print(f"Validation passed for package: {package_root}")
    for line in info:
        print(f"- {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
