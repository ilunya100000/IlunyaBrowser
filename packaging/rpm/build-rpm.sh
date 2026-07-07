#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VERSION="$(tr -d '[:space:]' < "${ROOT}/VERSION")"
SPEC="${ROOT}/packaging/rpm/ilunyabrowser.spec"
DIST_DIR="${ROOT}/packaging/dist"
TARBALL="${DIST_DIR}/ilunyabrowser-${VERSION}.tar.gz"
RPMBUILD="${ROOT}/packaging/rpmbuild"

if ! command -v rpmbuild >/dev/null 2>&1; then
  echo "Install build tools first:"
  echo "  Fedora: sudo dnf install rpm-build python3-pyqt6 python3-pyqt6-webengine"
  echo "  RHEL:   sudo dnf install rpm-build python3-qt6 python3-qt6-webengine"
  exit 1
fi

"${ROOT}/packaging/make-dist.sh"

mkdir -p "${RPMBUILD}"/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
cp "${TARBALL}" "${RPMBUILD}/SOURCES/"
cp "${SPEC}" "${RPMBUILD}/SPECS/"

rpmbuild \
  --define "_topdir ${RPMBUILD}" \
  -bb "${RPMBUILD}/SPECS/ilunyabrowser.spec"

echo
echo "RPM packages:"
find "${RPMBUILD}/RPMS" -name '*.rpm' -print
