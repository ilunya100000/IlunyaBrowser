#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
KEY="${ROOT}/.aur-deploy/aur"
AUR_DIR="${ROOT}/packaging/aur"
PKGNAME="ilunyabrowser"
VERSION="$(tr -d '[:space:]' < "${ROOT}/VERSION")"
TAG="v${VERSION}"
TMP="$(mktemp -d)"

cleanup() { rm -rf "${TMP}"; }
trap cleanup EXIT

if [[ ! -f "${KEY}" ]]; then
  echo "Missing ${KEY}. Run scripts/setup-aur.ps1 first."
  exit 1
fi

export GIT_SSH_COMMAND="ssh -i ${KEY} -o StrictHostKeyChecking=accept-new"

SHA256="$(curl -fsSL "https://github.com/ilunya100000/IlunyaBrowser/archive/refs/tags/${TAG}.tar.gz" | sha256sum | awk '{print $1}')"

cd "${AUR_DIR}"
sed -i "s/^pkgver=.*/pkgver=${VERSION}/" PKGBUILD
sed -i "s|refs/tags/v[^.]*|refs/tags/${TAG}|" PKGBUILD
sed -i "s/sha256sums=('.*')/sha256sums=('${SHA256}')/" PKGBUILD
makepkg --printsrcinfo > .SRCINFO

if git ls-remote "ssh://aur@aur.archlinux.org/${PKGNAME}.git" >/dev/null 2>&1; then
  git clone "ssh://aur@aur.archlinux.org/${PKGNAME}.git" "${TMP}/${PKGNAME}"
else
  mkdir -p "${TMP}/${PKGNAME}"
  cd "${TMP}/${PKGNAME}"
  git init
  git remote add origin "ssh://aur@aur.archlinux.org/${PKGNAME}.git"
  git checkout -b master
  cd -
fi

cp "${AUR_DIR}/PKGBUILD" "${AUR_DIR}/.SRCINFO" "${TMP}/${PKGNAME}/"
cd "${TMP}/${PKGNAME}"
git add PKGBUILD .SRCINFO
git -c user.name="ilunya100000" -c user.email="ilunya100000@users.noreply.github.com" \
  commit -m "Release ${VERSION}" || true
git push -u origin master

echo "Published to https://aur.archlinux.org/packages/${PKGNAME}"
echo "Install with: yay -S ${PKGNAME}"
