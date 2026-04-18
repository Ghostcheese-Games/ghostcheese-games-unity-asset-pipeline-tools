#!/usr/bin/env python3
"""Integration tests for the UI Toolkit graphics package validator slice."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[3]
    cases_path = repo_root / "tests" / "integration" / "ui-toolkit-graphics-package-validator" / "cases.json"
    with cases_path.open("r", encoding="utf-8") as handle:
        spec = json.load(handle)

    validator = repo_root / spec["validator"]
    cases = spec["cases"]

    failures: list[str] = []
    skipped: list[str] = []
    for case in cases:
        package_root = repo_root / case["packageRoot"]
        if case["name"] == "invalid-symlink-escape":
            symlink_path = package_root / "Linked"
            if not symlink_path.is_symlink():
                skipped.append(f"{case['name']}: skipped because {symlink_path} is not a symlink on this platform.")
                continue
        command = [sys.executable, str(validator), "--package-root", str(package_root)]
        manifest_name = case.get("manifestName")
        if manifest_name is not None:
            command.extend(["--manifest-name", manifest_name])
        result = subprocess.run(
            command,
            cwd=repo_root,
            check=False,
            capture_output=True,
            text=True,
        )
        output = f"{result.stdout}\n{result.stderr}".strip()
        is_valid = result.returncode == 0
        if is_valid != case["expectValid"]:
            failures.append(
                f"{case['name']}: expected valid={case['expectValid']}, got valid={is_valid}. Output:\n{output}"
            )
            continue

        expected_fragment = case.get("expectedOutputContains")
        if expected_fragment and expected_fragment not in output:
            failures.append(
                f"{case['name']}: expected output to contain {expected_fragment!r}. Output:\n{output}"
            )

    if failures:
        print("UI Toolkit graphics package validator integration tests failed:")
        for failure in failures:
            print(f"- {failure}")
        if skipped:
            print("Skipped cases:")
            for skip in skipped:
                print(f"- {skip}")
        return 1

    executed_count = len(cases) - len(skipped)
    print(f"UI Toolkit graphics package validator integration tests passed ({executed_count}/{len(cases)} cases).")
    if skipped:
        print("Skipped cases:")
        for skip in skipped:
            print(f"- {skip}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
