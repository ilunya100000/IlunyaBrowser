#!/usr/bin/env bash
# Publish ilunyabrowser to AUR (requires AUR account + SSH key).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AUR_DIR="${ROOT}/packaging/aur"
PKGNAME="ilunyabrowser"
TMP="$(mktemp -d)"

cleanup() { rm -rf "${TMP}"; }
trap cleanup EXIT

if ! command -v makepkg >/dev/null 2>&1; then
  echo "makepkg not found. Run this on Arch Linux."
  exit 1
fi

cd "${AUR_DIR}"
makepkg --printsrcinfo > .SRCINFO
updpkgsums || true

git clone "ssh://aur@aur.archlinux.org/${PKGNAME}.git" "${TMP}/${PKGNAME}" 2>/dev/null || {
  mkdir -p "${TMP}/${PKGNAME}"
  cd "${TMP}/${PKGNAME}"
  git init
  git remote add origin "ssh://aur@aur.archlinux.org/${PKGNAME}.git"
  git checkout -b master
}

cp "${AUR_DIR}/PKGBUILD" "${AUR_DIR}/.SRCINFO" "${TMP}/${PKGNAME}/"
cd "${TMP}/${PKGNAME}"
git add PKGBUILD .SRCINFO
git commit -m "Release $(grep '^pkgver=' PKGBUILD | cut -d= -f2)"
git push origin master

echo "AUR package updated: https://aur.archlinux.org/packages/${PKGNAME}"
echo "Install with: yay -S ${PKGNAME}"
