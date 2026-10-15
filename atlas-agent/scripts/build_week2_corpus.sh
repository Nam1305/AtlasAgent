#!/usr/bin/env bash
# Regenerate the Week 2 corpus manifest and check that every fixture exists.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python - <<'PY'
import json
from pathlib import Path

manifest = Path("data/raw/week2_eval/corpus_manifest.json")
data = json.loads(manifest.read_text())
missing = [d["file"] for d in data["documents"] if not (Path("data/raw/week2_eval") / d["file"]).exists()]
if missing:
    raise SystemExit(f"Missing corpus files: {missing}")
print(f"OK: {len(data['documents'])} corpus entries present")
PY
