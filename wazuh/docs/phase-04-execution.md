# Phase 04 — Execution (Wazuh Wiring)

Status: **scaffolded** (not validated against live telemetry yet).

## Log source
All Phase 04 scripts write to a shared log file:

- `artifacts/phase-04-execution/ptclab.log`

Each event line looks like:
```
PTCLAB phase=execution technique=T1059.004 script=lolbin_execution event=command message="/bin/sh -c id"
```

## Agent configuration (example)
Add a `localfile` entry on the agent that runs the scripts:

```xml
<localfile>
  <log_format>full_log</log_format>
  <location>/path/to/artifacts/phase-04-execution/ptclab.log</location>
</localfile>
```

## Decoders and rules
- Decoder: `wazuh/decoders/phase-04-execution.xml`
- Rules: `wazuh/rules/phase-04-execution.xml`

## Expected alert behavior
- Rule `100401`: shell execution event
- Rule `100402`: base64-encoded command event
- Rule `100403`: interpreter execution event

## Validation
Export alerts from Wazuh and run:
```bash
python3 runner/validate_wazuh.py --alerts /path/to/alerts.json
```

If you haven’t configured Wazuh yet, keep this file as the wiring plan.
