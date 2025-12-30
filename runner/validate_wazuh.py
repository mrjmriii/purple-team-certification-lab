#!/usr/bin/env python3
"""Validate Wazuh alerts against expected rule IDs."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from datetime import datetime


def load_alerts(path: pathlib.Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return data
        return [data]
    except json.JSONDecodeError:
        alerts = []
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            alerts.append(json.loads(line))
        return alerts


def load_expected(manifest_path: pathlib.Path, expected_override: list[int]) -> list[int]:
    if expected_override:
        return expected_override
    if not manifest_path.exists():
        return []
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return manifest.get("expected_rule_ids", [])


def extract_rule_id(alert: dict) -> int | None:
    rule = alert.get("rule", {})
    rule_id = rule.get("id")
    if isinstance(rule_id, str) and rule_id.isdigit():
        return int(rule_id)
    if isinstance(rule_id, int):
        return rule_id
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Wazuh alerts for a phase.")
    parser.add_argument("--alerts", required=True, help="Path to Wazuh alert export JSON.")
    parser.add_argument(
        "--manifest",
        default="labs/phase-04-execution/manifest.json",
        help="Manifest with expected rule IDs.",
    )
    parser.add_argument(
        "--expected",
        nargs="*",
        type=int,
        default=[],
        help="Override expected rule IDs.",
    )
    parser.add_argument(
        "--output",
        default="artifacts/phase-04-execution/validation_report.json",
        help="Where to write validation output.",
    )
    args = parser.parse_args()

    alerts_path = pathlib.Path(args.alerts)
    alerts = load_alerts(alerts_path)
    expected = load_expected(pathlib.Path(args.manifest), args.expected)

    seen = []
    for alert in alerts:
        rule_id = extract_rule_id(alert)
        if rule_id is not None:
            seen.append(rule_id)

    results = {
        "manifest": args.manifest,
        "alerts": str(alerts_path),
        "expected_rule_ids": expected,
        "seen_rule_ids": sorted(set(seen)),
        "missing_rule_ids": sorted(set(expected) - set(seen)),
        "total_alerts": len(alerts),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
