#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="$(tr -d '[:space:]' < "${ROOT}/VERSION")"

cd "${ROOT}/packaging/aur"
SHA256="$(curl -fsSL "https://github.com/ilunya100000/IlunyaBrowser/archive/refs/tags/v${VERSION}.tar.gz" | sha256sum | awk '{print $1}')"
sed -i "s/^pkgver=.*/pkgver=${VERSION}/" PKGBUILD
sed -i "s|refs/tags/v[^\"]*|refs/tags/v${VERSION}|" PKGBUILD
sed -i "s/sha256sums=('.*')/sha256sums=('${SHA256}')/" PKGBUILD
makepkg --printsrcinfo > .SRCINFO

echo "Updated packaging/aur for v${VERSION}"
