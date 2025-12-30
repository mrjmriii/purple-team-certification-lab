#!/usr/bin/env python3
"""Drop and execute a temp script via the Python interpreter."""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys
from datetime import datetime

PHASE = "execution"
SCRIPT = "script_interpreter_abuse"
TECHNIQUE = "T1059.006"


def resolve_workspace(path: str, allow_outside: bool) -> pathlib.Path:
    workspace = pathlib.Path(path).expanduser().resolve()
    allowed_roots = [pathlib.Path.cwd() / "artifacts", pathlib.Path("/tmp")]
    if not allow_outside:
        if not any(str(workspace).startswith(str(root.resolve())) for root in allowed_roots):
            raise SystemExit(
                f"Workspace '{workspace}' is outside allowed roots. "
                "Use --allow-outside-workspace to override."
            )
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace


def log_event(log_path: pathlib.Path, event: str, message: str) -> None:
    safe_message = message.replace('"', "'")
    line = (
        f"PTCLAB phase={PHASE} technique={TECHNIQUE} script={SCRIPT} "
        f"event={event} message=\"{safe_message}\""
    )
    print(line)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Simulate interpreter execution.")
    parser.add_argument(
        "--workspace",
        default="artifacts/phase-04-execution",
        help="Workspace directory for artifacts.",
    )
    parser.add_argument(
        "--allow-outside-workspace",
        action="store_true",
        help="Allow writing outside the default workspace roots.",
    )
    args = parser.parse_args()

    workspace = resolve_workspace(args.workspace, args.allow_outside_workspace)
    log_path = workspace / "ptclab.log"
    script_path = workspace / "tmp_runner.py"
    output_path = workspace / "script.out"

    payload = (
        "from datetime import datetime\n"
        "print('ptclab script execution')\n"
        "print(datetime.utcnow().isoformat() + 'Z')\n"
    )

    log_event(log_path, "start", f"workspace={workspace}")
    script_path.write_text(payload, encoding="utf-8")
    log_event(log_path, "write", f"script={script_path}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    output_path.write_text(result.stdout, encoding="utf-8")

    log_event(log_path, "output", f"wrote={output_path}")
    log_event(log_path, "complete", "ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
