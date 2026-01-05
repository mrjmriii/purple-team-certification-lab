# Purple Team Certification Lab
AI-assisted, human-directed purple-team lab that validates Wazuh detections across
all MITRE ATT&CK phases using phase-driven adversary emulation.

This repository is a companion to `iac-homelab` (infra baselines + lab orchestration).

![Purple Team Certification Lab overview](wazuh/assets/purple-team-overview.svg)

## Lab snapshot
- Phase-driven adversary emulation (MITRE ATT&CK kill-chain coverage)
- Wazuh-only detection validation (no commercial tooling)
- Telemetry-first scripts with explicit expected outcomes

## How to read it
1. Start with `labs/` for per-phase scripts and writeups
2. Review `wazuh/` for detection docs, rules, and decoders
3. Use `runner/` to execute phases and validate alerts
4. Check `scoring/` for pass/fail criteria

## Structure (high level)
- `labs/`: per-phase scripts and writeups
- `wazuh/`: decoders, rules, dashboards, and detection docs
- `runner/`: automation harness for running phases + validating alerts
- `scoring/`: pass/fail criteria

## Assumptions and limitations
- Wazuh-only detection focus; Linux first
- Safe, non-destructive simulations by default
- No commercial tooling, no exploitation of real vulnerabilities
- One technique per script, prioritized for observability

## Current status
- Phase 04 (Execution) scaffolded with scripts, manifest, Wazuh wiring, and validation stub
- Other phases planned

## Quickstart (Phase 04)
```bash
python3 runner/run_phase.py --manifest labs/phase-04-execution/manifest.json --workspace artifacts/phase-04-execution
```

To validate against exported alerts:
```bash
python3 runner/validate_wazuh.py --alerts /path/to/alerts.json
```

## AI-assisted development
This repo is built with AI assistance. See `AGENTS.conf` for the exact execution contract
and guardrails.

## Public repo hygiene
- No internal IPs, hostnames, or secrets are stored here
- Use documentation-safe examples like `example.com` or `192.0.2.0/24`

## Companion repository
- https://github.com/mrjmriii/iac-homelab
