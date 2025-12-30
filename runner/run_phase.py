#!/usr/bin/env python3
"""Run a phase manifest and capture execution metadata."""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from datetime import datetime


def load_manifest(path: pathlib.Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def ensure_workspace(path: pathlib.Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def run_script(script_path: pathlib.Path, workspace: str, allow_outside: bool) -> dict:
    cmd = [sys.executable, str(script_path), "--workspace", workspace]
    if allow_outside:
        cmd.append("--allow-outside-workspace")
    started = datetime.utcnow().isoformat() + "Z"
    result = subprocess.run(cmd, capture_output=True, text=True)
    finished = datetime.utcnow().isoformat() + "Z"
    return {
        "script": str(script_path),
        "command": " ".join(cmd),
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "started": started,
        "finished": finished,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a phase manifest.")
    parser.add_argument(
        "--manifest",
        default="labs/phase-04-execution/manifest.json",
        help="Path to phase manifest JSON.",
    )
    parser.add_argument(
        "--workspace",
        default="artifacts/phase-04-execution",
        help="Workspace directory for artifacts.",
    )
    parser.add_argument(
        "--allow-outside-workspace",
        action="store_true",
        help="Allow scripts to write outside the default workspace roots.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned commands without executing.",
    )
    args = parser.parse_args()

    manifest_path = pathlib.Path(args.manifest)
    manifest = load_manifest(manifest_path)

    workspace = pathlib.Path(args.workspace)
    ensure_workspace(workspace)

    run_report = {
        "phase": manifest.get("id"),
        "manifest": str(manifest_path),
        "workspace": str(workspace),
        "started": datetime.utcnow().isoformat() + "Z",
        "scripts": [],
    }

    for entry in manifest.get("scripts", []):
        script_path = pathlib.Path(entry["path"])
        if args.dry_run:
            print(f"DRY RUN: {script_path}")
            continue
        run_report["scripts"].append(
            run_script(script_path, args.workspace, args.allow_outside_workspace)
        )

    run_report["finished"] = datetime.utcnow().isoformat() + "Z"
    report_path = workspace / "run_report.json"
    report_path.write_text(json.dumps(run_report, indent=2), encoding="utf-8")
    print(f"Run report: {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
