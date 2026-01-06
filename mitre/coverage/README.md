# Validation Coverage (Planned vs Actual)

This directory captures the validation-first MITRE ATT&CK coverage state.
Planned coverage is derived from `mitre/kill_chain_maps.md`; actual coverage is
populated as certification plays are validated.

## Sources of truth
- Planned coverage: `mitre/kill_chain_maps.md` (technique IDs in posture tables)
- Actual coverage: `mitre/coverage/actual.json` (validated techniques only)
- Official ATT&CK data: https://github.com/mitre-attack/attack-stix-data

## Actual coverage format
`mitre/coverage/actual.json` accepts either strings or objects.
Only entries marked `status: validated` are included in the actual map.

Example:
```json
{
  "updated_at": "2026-01-06",
  "techniques": [
    "T1059",
    {
      "id": "T1562.001",
      "status": "validated",
      "evidence": ["labs/phase-04-execution/manifest.json#T1562.001"],
      "notes": "Wazuh alert validated in lab run 2026-01-06"
    }
  ]
}
```

## Build workflow
1. Fetch the official ATT&CK STIX data (network required, disabled by default):
   `mitre/tools/fetch_attack_stix.sh`
2. Update `mitre/coverage/actual.json` when a technique is fully validated.
3. Regenerate coverage assets:
   `python3 mitre/tools/build_coverage_assets.py`

## Outputs
- `mitre/navigator/coverage_planned.json`
- `mitre/navigator/coverage_actual.json`
- `mitre/navigator/previews/coverage_planned.svg` (+ `.dark.svg`)
- `mitre/navigator/previews/coverage_actual.svg` (+ `.dark.svg`)

## Validation checklist
- Import the JSON layers into https://mitre-attack.github.io/attack-navigator/
  and confirm the techniques highlight under the correct tactics.
- Open the SVG previews in GitHub and confirm light/dark rendering.
