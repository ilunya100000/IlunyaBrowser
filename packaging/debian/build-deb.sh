#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DEBIAN_DIR="${ROOT}/packaging/debian"

if ! command -v dpkg-buildpackage >/dev/null 2>&1; then
  echo "Install build tools first:"
  echo "  sudo apt install build-essential debhelper dh-python python3-all python3-pyqt6 python3-pyqt6.qtwebengine"
  exit 1
fi

cd "${ROOT}"
rm -rf debian
cp -a "${DEBIAN_DIR}" debian
chmod +x debian/rules

dpkg-buildpackage -us -uc -b
echo
echo "Packages created in $(dirname "${ROOT}")"
