# Phase 04: Execution

Objective: simulate command and scripting execution in a safe, observable way.

Status: **scaffolded** (not validated against live detections yet).

## Techniques covered
- T1059.004 — Command and Scripting Interpreter: Unix Shell
- T1059.006 — Command and Scripting Interpreter: Python
- T1027 — Obfuscated/Encoded Files or Information

## Scripts
- `scripts/lolbin_execution.py`
  - Simulates shell command execution (living-off-the-land style).
- `scripts/encoded_command_exec.py`
  - Executes a base64-encoded command.
- `scripts/script_interpreter_abuse.py`
  - Drops and executes a temp script via the Python interpreter.

## Expected telemetry
- Process creation for `/bin/sh`, `python3`, and child commands.
- File writes in the phase workspace.
- Command-line strings containing encoded payloads.

## How to run (manual)
```bash
python3 labs/phase-04-execution/scripts/lolbin_execution.py --workspace artifacts/phase-04-execution
python3 labs/phase-04-execution/scripts/encoded_command_exec.py --workspace artifacts/phase-04-execution
python3 labs/phase-04-execution/scripts/script_interpreter_abuse.py --workspace artifacts/phase-04-execution
```

## How to run (runner)
```bash
python3 runner/run_phase.py --manifest labs/phase-04-execution/manifest.json --workspace artifacts/phase-04-execution
```

## Detection goals
- Flag interpreter execution with suspicious command-lines.
- Flag base64-encoded command execution.
- Flag scripts executed from temporary or non-standard paths.

## Safety
- Scripts only write to a workspace under `./artifacts/` or `/tmp` by default.
- Use `--allow-outside-workspace` if you need to write elsewhere.
