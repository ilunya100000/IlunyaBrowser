#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OVERLAY="${ROOT}/packaging/gentoo-overlay"
REPO="${OVERLAY}/ilunyabrowser"
EBUILD_DIR="${REPO}/www-client/ilunyabrowser"
FILESDIR="${EBUILD_DIR}/files"

mkdir -p "${EBUILD_DIR}" "${FILESDIR}"

cp "${ROOT}/packaging/gentoo/ilunyabrowser-"*".ebuild" "${EBUILD_DIR}/"
cp "${ROOT}/packaging/gentoo/metadata.xml" "${EBUILD_DIR}/"
cp "${ROOT}/packaging/linux/ilunyabrowser" "${FILESDIR}/"
cp "${ROOT}/packaging/linux/ilunyabrowser.desktop" "${FILESDIR}/"

cat > "${REPO}/profiles/repo_name" <<'EOF'
ilunyabrowser
EOF

cat > "${REPO}/metadata/layout.conf" <<'EOF'
masters = gentoo
EOF

echo "Gentoo overlay prepared at: ${REPO}"
echo
echo "Install:"
echo "  sudo eselect repository enable ilunyabrowser"
echo "  sudo emerge --sync ilunyabrowser"
echo "  sudo emerge -av www-client/ilunyabrowser"
echo
echo "Or add as local overlay:"
echo "  sudo eselect repository add ilunyabrowser ${REPO}"
echo "  sudo emerge --sync ilunyabrowser"
echo "  sudo emerge -av www-client/ilunyabrowser"
