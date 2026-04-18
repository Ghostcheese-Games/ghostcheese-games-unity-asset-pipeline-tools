#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${repo_root}"

echo "Running lightweight repository validation baseline..."

required_paths=(
  "README.md"
  "docs"
  "tools"
  "schemas"
  "examples"
  "fixtures"
  "tests"
  "scripts"
)

for path in "${required_paths[@]}"; do
  if [[ ! -e "${path}" ]]; then
    echo "Missing required repo path: ${path}" >&2
    exit 1
  fi
done

required_readmes=(
  "docs/README.md"
  "tools/README.md"
  "schemas/README.md"
  "examples/README.md"
  "fixtures/README.md"
  "tests/README.md"
  "scripts/README.md"
)

for readme in "${required_readmes[@]}"; do
  if [[ ! -f "${readme}" ]]; then
    echo "Missing required README: ${readme}" >&2
    exit 1
  fi
done

mapfile -t markdown_files < <(git --no-pager ls-files "*.md")
if [[ "${#markdown_files[@]}" -eq 0 ]]; then
  echo "No markdown files found; expected documentation files." >&2
  exit 1
fi

for file in "${markdown_files[@]}"; do
  first_non_empty_line="$(grep -m1 -E '[^[:space:]]' "${file}" || true)"
  if [[ -z "${first_non_empty_line}" ]]; then
    echo "Markdown file is empty: ${file}" >&2
    exit 1
  fi

  if [[ "${first_non_empty_line}" != "#"* ]]; then
    echo "Markdown file must start with a heading: ${file}" >&2
    exit 1
  fi
done

while IFS= read -r -d '' script; do
  bash -n "${script}"
done < <(find scripts -type f -name "*.sh" -print0)

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 command not found. Please install Python 3.10+ and retry." >&2
  exit 1
fi

if ! python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'; then
  echo "Python 3.10+ is required to run integration validation. Current version: $(python3 -V 2>&1)." >&2
  exit 1
fi

python3 tests/integration/ui-toolkit-graphics-package-validator/test_validator.py

echo "Validation passed."
