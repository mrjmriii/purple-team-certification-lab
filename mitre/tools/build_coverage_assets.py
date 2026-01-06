#!/usr/bin/env python3
"""Build planned vs actual MITRE coverage layers and SVG previews."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

TACTIC_ORDER = [
    "reconnaissance",
    "resource-development",
    "initial-access",
    "execution",
    "persistence",
    "privilege-escalation",
    "defense-evasion",
    "credential-access",
    "discovery",
    "lateral-movement",
    "collection",
    "command-and-control",
    "exfiltration",
    "impact",
]

TACTIC_TITLES = {
    "reconnaissance": "Reconnaissance",
    "resource-development": "Resource Development",
    "initial-access": "Initial Access",
    "execution": "Execution",
    "persistence": "Persistence",
    "privilege-escalation": "Privilege Escalation",
    "defense-evasion": "Defense Evasion",
    "credential-access": "Credential Access",
    "discovery": "Discovery",
    "lateral-movement": "Lateral Movement",
    "collection": "Collection",
    "command-and-control": "Command and Control",
    "exfiltration": "Exfiltration",
    "impact": "Impact",
    "status": "Status",
}

VALIDATED_STATUSES = {"validated", "certified", "complete"}

TECHNIQUE_PATTERN = re.compile(r"T\d{4}(?:\.\d{3})?")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build planned vs actual MITRE coverage layers and previews."
    )
    parser.add_argument(
        "--stix-root",
        default="third_party/attack-stix-data",
        help="Path to attack-stix-data clone (default: third_party/attack-stix-data)",
    )
    parser.add_argument(
        "--planned-source",
        default="mitre/kill_chain_maps.md",
        help="Planned coverage source (default: mitre/kill_chain_maps.md)",
    )
    parser.add_argument(
        "--actual-source",
        default="mitre/coverage/actual.json",
        help="Actual coverage source (default: mitre/coverage/actual.json)",
    )
    parser.add_argument(
        "--output-dir",
        default="mitre/navigator",
        help="Navigator layer output directory (default: mitre/navigator)",
    )
    parser.add_argument(
        "--preview-dir",
        default="mitre/navigator/previews",
        help="SVG preview output directory (default: mitre/navigator/previews)",
    )
    parser.add_argument(
        "--attack-version",
        default="14",
        help="ATT&CK version label for Navigator layers (default: 14)",
    )
    parser.add_argument(
        "--navigator-version",
        default="4.8.1",
        help="Navigator version label for layers (default: 4.8.1)",
    )
    parser.add_argument(
        "--layer-version",
        default="4.4",
        help="Navigator layer schema version (default: 4.4)",
    )
    return parser.parse_args()


def tactic_sort_key(tactic: str) -> Tuple[int, str]:
    try:
        return (TACTIC_ORDER.index(tactic), tactic)
    except ValueError:
        return (len(TACTIC_ORDER), tactic)


def technique_sort_key(technique_id: str) -> Tuple[str, str]:
    parts = technique_id.split(".")
    base = parts[0]
    suffix = parts[1] if len(parts) > 1 else ""
    return (base, suffix)


def load_attack_techniques(stix_path: Path) -> Dict[str, Dict[str, object]]:
    with stix_path.open("r", encoding="utf-8") as handle:
        bundle = json.load(handle)

    techniques: Dict[str, Dict[str, object]] = {}
    for obj in bundle.get("objects", []):
        if obj.get("type") != "attack-pattern":
            continue
        if obj.get("revoked") or obj.get("x_mitre_deprecated"):
            continue

        ext_id = None
        for ref in obj.get("external_references", []):
            if ref.get("source_name") == "mitre-attack" and ref.get("external_id"):
                ext_id = ref.get("external_id")
                break
        if not ext_id:
            continue

        domains = obj.get("x_mitre_domains", [])
        if domains and "enterprise-attack" not in domains:
            continue

        tactics = []
        for phase in obj.get("kill_chain_phases", []):
            if phase.get("kill_chain_name") != "mitre-attack":
                continue
            phase_name = phase.get("phase_name")
            if phase_name and phase_name not in tactics:
                tactics.append(phase_name)

        techniques[ext_id] = {
            "name": obj.get("name", "Unknown"),
            "tactics": tactics,
        }

    return techniques


def extract_technique_ids_from_markdown(path: Path) -> List[str]:
    text = path.read_text(encoding="utf-8")
    return sorted(set(TECHNIQUE_PATTERN.findall(text)), key=technique_sort_key)


def load_actual_techniques(path: Path) -> List[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data.get("techniques", [])
    ids: List[str] = []

    for entry in entries:
        if isinstance(entry, str):
            ids.append(entry.strip())
            continue
        if isinstance(entry, dict):
            technique_id = (entry.get("id") or entry.get("technique_id") or "").strip()
            if not technique_id:
                continue
            status = str(entry.get("status", "validated")).lower()
            if status in VALIDATED_STATUSES:
                ids.append(technique_id)
            continue
    return sorted(set(ids), key=technique_sort_key)


def build_layer(
    name: str,
    description: str,
    technique_ids: Iterable[str],
    technique_map: Dict[str, Dict[str, object]],
    attack_version: str,
    navigator_version: str,
    layer_version: str,
    color_min: str,
    color_max: str,
) -> Tuple[Dict[str, object], List[str]]:
    techniques = []
    unknown = []

    for technique_id in sorted(set(technique_ids), key=technique_sort_key):
        details = technique_map.get(technique_id)
        if not details:
            unknown.append(technique_id)
            techniques.append(
                {
                    "techniqueID": technique_id,
                    "score": 1,
                    "enabled": True,
                }
            )
            continue

        tactics = details.get("tactics") or []
        if not tactics:
            techniques.append(
                {
                    "techniqueID": technique_id,
                    "score": 1,
                    "enabled": True,
                }
            )
            continue

        for tactic in sorted(tactics, key=tactic_sort_key):
            techniques.append(
                {
                    "techniqueID": technique_id,
                    "tactic": tactic,
                    "score": 1,
                    "enabled": True,
                }
            )

    layer = {
        "name": name,
        "description": description,
        "domain": "enterprise-attack",
        "versions": {
            "attack": attack_version,
            "navigator": navigator_version,
            "layer": layer_version,
        },
        "techniques": techniques,
        "gradient": {"colors": [color_min, color_max], "minValue": 0, "maxValue": 1},
        "selectTechniquesAcrossTactics": True,
        "showTacticRowBackground": False,
        "hideDisabled": True,
    }
    return layer, unknown


def build_tactic_groups(
    technique_ids: Iterable[str],
    technique_map: Dict[str, Dict[str, object]],
) -> Tuple[List[Tuple[str, List[Tuple[str, str]]]], List[str]]:
    grouped: Dict[str, List[Tuple[str, str]]] = {}
    unknown: List[str] = []

    for technique_id in sorted(set(technique_ids), key=technique_sort_key):
        details = technique_map.get(technique_id)
        if not details:
            unknown.append(technique_id)
            continue

        name = str(details.get("name", "Unknown"))
        tactics = details.get("tactics") or []
        if not tactics:
            grouped.setdefault("unmapped", []).append((technique_id, name))
            continue

        for tactic in tactics:
            grouped.setdefault(tactic, []).append((technique_id, name))

    if unknown:
        grouped.setdefault("unmapped", []).extend(
            [(technique_id, "Unknown") for technique_id in unknown]
        )

    ordered = []
    for tactic in TACTIC_ORDER:
        if tactic in grouped:
            ordered.append(
                (tactic, sorted(grouped[tactic], key=lambda item: technique_sort_key(item[0])))
            )
    for tactic in sorted(grouped.keys()):
        if tactic not in TACTIC_ORDER:
            ordered.append(
                (tactic, sorted(grouped[tactic], key=lambda item: technique_sort_key(item[0])))
            )

    return ordered, unknown


def xml_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def truncate(text: str, max_len: int) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def render_preview_svg(
    title: str,
    tactic_groups: List[Tuple[str, List[Tuple[str, str]]]],
    accent: str,
    dark: bool,
) -> str:
    width = 900
    x = 20
    card_width = 860
    y = 50
    card_gap = 20
    header_y = 30
    header_offset = 22
    line_start_offset = 40
    line_height = 16
    bottom_padding = 14
    corner = 10
    stroke_width = 2 if dark else 1.5
    fill_opacity = 0.28 if dark else 0.18

    if dark:
        bg = "<rect width='100%' height='100%' fill='#111827' />\n\n"
        text_color = "#f8fafc"
        sub_color = "#cbd5e1"
    else:
        bg = ""
        text_color = "#0f172a"
        sub_color = "#334155"

    if not tactic_groups:
        tactic_groups = [
            ("status", [("", "No validated techniques yet. Update mitre/coverage/actual.json.")])
        ]

    blocks = []
    current_y = y

    for tactic, items in tactic_groups:
        lines = []
        for technique_id, name in items:
            line = f"{technique_id} {name}".strip()
            lines.append(truncate(line, 78))

        title_text = TACTIC_TITLES.get(tactic, tactic.replace("-", " ").title())
        header_text = f"{title_text} ({len(items)})"

        card_height = line_start_offset + (line_height * len(lines)) + bottom_padding

        blocks.append(
            f"<rect x='{x}' y='{current_y}' width='{card_width}' height='{card_height}' "
            f"rx='{corner}' ry='{corner}' fill='{accent}' fill-opacity='{fill_opacity}' "
            f"stroke='{accent}' stroke-width='{stroke_width}' />"
        )
        blocks.append(
            f"<text x='{x + 20}' y='{current_y + header_offset}' class='hdr'>{xml_escape(header_text)}</text>"
        )

        text_y = current_y + line_start_offset
        for line in lines:
            blocks.append(
                f"<text x='{x + 20}' y='{text_y}' class='sub'>{xml_escape(line)}</text>"
            )
            text_y += line_height

        current_y += card_height + card_gap

    height = current_y + 20

    style = (
        f"<style>text{{font-family:Arial,Helvetica,sans-serif;font-size:14px;fill:{text_color};}} "
        f".hdr{{font-size:18px;font-weight:bold;}} "
        f".sub{{font-size:12px;fill:{sub_color};}}</style>"
    )

    content = "\n".join(blocks)
    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' "
        f"viewBox='0 0 {width} {height}'>\n"
        f"{bg}"
        f"{style}\n"
        f"<text x='20' y='{header_y}' class='hdr'>{xml_escape(title)}</text>\n"
        f"{content}\n"
        "</svg>\n"
    )


def write_json(path: Path, payload: Dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def main() -> int:
    args = parse_args()

    stix_root = Path(args.stix_root)
    stix_path = stix_root / "enterprise-attack" / "enterprise-attack.json"
    if not stix_path.exists():
        print(
            f"Missing ATT&CK STIX data at {stix_path}. "
            "Run mitre/tools/fetch_attack_stix.sh first.",
            file=sys.stderr,
        )
        return 1

    planned_source = Path(args.planned_source)
    actual_source = Path(args.actual_source)
    if not planned_source.exists():
        print(f"Planned source not found: {planned_source}", file=sys.stderr)
        return 1
    if not actual_source.exists():
        print(f"Actual source not found: {actual_source}", file=sys.stderr)
        return 1

    technique_map = load_attack_techniques(stix_path)

    planned_ids = extract_technique_ids_from_markdown(planned_source)
    actual_ids = load_actual_techniques(actual_source)

    output_dir = Path(args.output_dir)
    preview_dir = Path(args.preview_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    preview_dir.mkdir(parents=True, exist_ok=True)

    planned_layer, planned_unknown = build_layer(
        name="Planned validation-first coverage",
        description="Planned validation-first coverage derived from mitre/kill_chain_maps.md",
        technique_ids=planned_ids,
        technique_map=technique_map,
        attack_version=args.attack_version,
        navigator_version=args.navigator_version,
        layer_version=args.layer_version,
        color_min="#e8f1ff",
        color_max="#2563eb",
    )

    actual_layer, actual_unknown = build_layer(
        name="Actual validation-first coverage",
        description="Validated techniques listed in mitre/coverage/actual.json",
        technique_ids=actual_ids,
        technique_map=technique_map,
        attack_version=args.attack_version,
        navigator_version=args.navigator_version,
        layer_version=args.layer_version,
        color_min="#e6f7ee",
        color_max="#16a34a",
    )

    write_json(output_dir / "coverage_planned.json", planned_layer)
    write_json(output_dir / "coverage_actual.json", actual_layer)

    planned_groups, _ = build_tactic_groups(planned_ids, technique_map)
    actual_groups, _ = build_tactic_groups(actual_ids, technique_map)

    planned_light = render_preview_svg(
        "Planned validation-first coverage",
        planned_groups,
        accent="#2563eb",
        dark=False,
    )
    planned_dark = render_preview_svg(
        "Planned validation-first coverage",
        planned_groups,
        accent="#2563eb",
        dark=True,
    )
    actual_light = render_preview_svg(
        "Actual validation-first coverage",
        actual_groups,
        accent="#16a34a",
        dark=False,
    )
    actual_dark = render_preview_svg(
        "Actual validation-first coverage",
        actual_groups,
        accent="#16a34a",
        dark=True,
    )

    write_text(preview_dir / "coverage_planned.svg", planned_light)
    write_text(preview_dir / "coverage_planned.dark.svg", planned_dark)
    write_text(preview_dir / "coverage_actual.svg", actual_light)
    write_text(preview_dir / "coverage_actual.dark.svg", actual_dark)

    if planned_unknown or actual_unknown:
        unknown = sorted(set(planned_unknown + actual_unknown), key=technique_sort_key)
        print(
            "Warning: unknown technique IDs (not found in ATT&CK STIX data): "
            + ", ".join(unknown),
            file=sys.stderr,
        )

    print("Coverage assets generated:")
    print(f"- {output_dir / 'coverage_planned.json'}")
    print(f"- {output_dir / 'coverage_actual.json'}")
    print(f"- {preview_dir / 'coverage_planned.svg'}")
    print(f"- {preview_dir / 'coverage_planned.dark.svg'}")
    print(f"- {preview_dir / 'coverage_actual.svg'}")
    print(f"- {preview_dir / 'coverage_actual.dark.svg'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
