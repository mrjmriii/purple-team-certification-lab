#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DEST_DIR="${ROOT_DIR}/third_party/attack-stix-data"
REPO_URL="https://github.com/mitre-attack/attack-stix-data.git"

if [[ -d "${DEST_DIR}/.git" ]]; then
  git -C "${DEST_DIR}" pull --ff-only
else
  git clone --depth 1 --filter=blob:none "${REPO_URL}" "${DEST_DIR}"
fi

echo "ATT&CK STIX data available at ${DEST_DIR}"
