# Purple Team Lab Planning (Pseudocode Emporium)

This document captures the planning artifacts produced during ideation. It is intentionally
pseudo/structural so it can evolve into concrete scripts, Wazuh rules, and a runner
while honoring the safety and telemetry guardrails in `AGENTS.conf`.

## Goals
- Map social-engineering postures to MITRE ATT&CK kill-chain phases and techniques.
- Define posture manifests that describe pretext, drift change, assumed access, scripts to run,
  expected telemetry, and expected Wazuh alerts.
- Keep simulations safe, deterministic, and telemetry-first (stdout logs, temp paths, localhost
  network only) until concrete implementations are added.
- Provide a foundation for a runner CLI that assembles phase/technique scripts based on posture
  manifests and emits a JSON report.
- Seed Wazuh detection ideas (Sigma-style) without final decoders/rules yet.

## Structure being created
- `labs/postures/`: Posture manifest schema and the 12 social-engineering posture manifests.
- `mitre/attack_matrix.yaml`: Planned mapping of phases to techniques and planned script names,
  annotated with posture IDs that invoke them.
- `mitre/phase_coverage.md`: Coverage table showing posture → phase → technique → planned scripts.
- `scoring/detection_scorecard.yaml`: Stubbed pass/fail criteria tying execution to expected alerts.
- `runner/`: Placeholder directory for future runner CLI.
- `wazuh/`: Placeholder for decoders/rules; current content is planning only.
- `mitre/kill_chain_maps.md`: Executive-ready per-posture MITRE kill-chain tables (phase, technique, planned script) plus Mermaid flows to visualize coverage quickly.
- `mitre/navigator/*.json`: ATT&CK Navigator layers for each posture; import into the MITRE ATT&CK Navigator web UI for tactic-aligned tiles with ordering metadata.
- `mitre/navigator/previews/*.svg`: GitHub-renderable previews generated from the Navigator layers so visitors can see the ordered steps without leaving the repo.

## Safety and scope
- Wazuh-only, Linux-first, non-destructive simulations. No real exploits or secrets.
- One technique per script; explicit logging; temp paths (e.g., `/tmp/purple-*`); localhost network
  for C2/exfil analogs.
- Use RFC5737/reserved IP ranges for any network simulation (e.g., 198.51.100.0/24).

## Next implementation steps (suggested)
1. Implement the first 3–5 scripts from posture manifests (e.g., postures 01, 02, 08) using the
   provided `_SIM` log markers and temp paths.
2. Add Wazuh decoders/rules that key off the `_SIM` markers; scope to lab hosts/users and
   time-box detections.
3. Build a runner skeleton that reads a posture manifest, executes scripts in order, captures
   stdout/stderr/artifacts, and writes a JSON report (include expected vs. observed alerts stub).
4. Expand the scorecard to assert pass/fail per posture: script exit 0 + artifact present +
   (future) Wazuh alert observed within window.

## References
- Guardrails and operating model: `AGENTS.conf`
- Public hygiene and AI transparency: `README.md`
