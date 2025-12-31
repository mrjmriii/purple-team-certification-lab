# Runner (planning stub)

Intended responsibilities:
- Accept posture ID/manifest and phase selection.
- Execute mapped scripts sequentially, capture stdout/stderr, store artifacts under /tmp or ./artifacts.
- Emit JSON report with per-script status, timestamps, and expected vs. observed alerts (observed alert checks are TODO until Wazuh integration is built).
- Support dry-run to list scripts without executing.

Current state: planning only; scripts and runner code not implemented.
