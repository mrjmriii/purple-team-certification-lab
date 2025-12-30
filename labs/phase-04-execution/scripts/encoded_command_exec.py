#!/usr/bin/env python3
"""Execute a base64-encoded shell command to simulate obfuscated execution."""
from __future__ import annotations

import argparse
import base64
import pathlib
import subprocess
import sys
from datetime import datetime

PHASE = "execution"
SCRIPT = "encoded_command_exec"
TECHNIQUE = "T1027"


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
    parser = argparse.ArgumentParser(description="Simulate encoded command execution.")
    parser.add_argument(
        "--workspace",
        default="artifacts/phase-04-execution",
        help="Workspace directory for artifacts.",
    )
    parser.add_argument(
        "--payload",
        default="echo ptclab encoded execution",
        help="Payload command to encode and execute.",
    )
    parser.add_argument(
        "--allow-outside-workspace",
        action="store_true",
        help="Allow writing outside the default workspace roots.",
    )
    args = parser.parse_args()

    workspace = resolve_workspace(args.workspace, args.allow_outside_workspace)
    log_path = workspace / "ptclab.log"
    output_path = workspace / "encoded.out"

    encoded = base64.b64encode(args.payload.encode("utf-8")).decode("utf-8")
    command = f"printf '%s' {encoded} | base64 --decode | /bin/sh"

    log_event(log_path, "start", f"workspace={workspace}")
    log_event(log_path, "encoded", f"base64={encoded}")
    log_event(log_path, "command", command)

    result = subprocess.run(
        ["/bin/sh", "-c", command],
        check=True,
        capture_output=True,
        text=True,
    )
    timestamp = datetime.utcnow().isoformat() + "Z"
    output_path.write_text(f"[{timestamp}]\n{result.stdout}\n", encoding="utf-8")

    log_event(log_path, "output", f"wrote={output_path}")
    log_event(log_path, "complete", "ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
