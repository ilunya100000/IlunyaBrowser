# Copyright 1999-2026 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=8

inherit desktop xdg

DESCRIPTION="Minimal Chromium-based browser focused on low RAM usage"
HOMEPAGE="https://github.com/izosi/IlunyaBrowser"
SRC_URI="https://github.com/izosi/IlunyaBrowser/archive/v${PV}.tar.gz -> ${P}.tar.gz"

LICENSE="MIT"
SLOT="0"
KEYWORDS="~amd64 ~arm64"
IUSE=""

RDEPEND="
	dev-python/PyQt6:=[webengine]
"

S="${WORKDIR}/IlunyaBrowser-${PV}"

src_install() {
	insinto /usr/share/ilunyabrowser
	doins ilunya_browser.py make_icon.py requirements-linux.txt VERSION

	exeinto /usr/bin
	doexe "${FILESDIR}/ilunyabrowser"

	domenu "${FILESDIR}/ilunyabrowser.desktop"
	doicon -s 256 assets/icon.png
}
