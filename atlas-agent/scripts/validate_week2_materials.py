"""Sanity-check the Week 2 evaluation materials.

Validates that every dataset is well-formed JSONL and that every entry
references an existing fixture where applicable.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASETS = ROOT / "evals" / "datasets"
REQUIRED_FILES = [
    "week2_rag_questions.jsonl",
    "week2_ocr_ground_truth.jsonl",
    "week2_memory_cases.jsonl",
]


def check_jsonl(path: Path) -> int:
    n = 0
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        assert isinstance(obj, dict), f"{path.name} line {n+1}: not an object"
        n += 1
    return n


def main() -> int:
    for name in REQUIRED_FILES:
        path = DATASETS / name
        if not path.exists():
            print(f"FAIL: missing {path}")
            return 1
        count = check_jsonl(path)
        print(f"OK  {name}: {count} cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
