#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="$(tr -d '[:space:]' < "${ROOT}/VERSION")"
NAME="ilunyabrowser"
DIST="${ROOT}/packaging/dist"
TARBALL="${DIST}/${NAME}-${VERSION}.tar.gz"

mkdir -p "${DIST}"

tar -czf "${TARBALL}" \
  --exclude='.git' \
  --exclude='.venv' \
  --exclude='dist' \
  --exclude='build' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='packaging/dist' \
  -C "${ROOT}" \
  ilunya_browser.py \
  make_icon.py \
  assets \
  requirements-linux.txt \
  VERSION \
  packaging/linux

echo "Created ${TARBALL}"
sha256sum "${TARBALL}" || shasum -a 256 "${TARBALL}"
