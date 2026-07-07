# IlunyaBrowser

Minimal Chromium-based browser (Qt WebEngine) focused on low RAM usage.

Features:
- Google homepage and search
- Multiple tabs with inactive tab unloading
- No bookmarks, extensions, sync, or other bloat

## Windows

Download **IlunyaBrowser.exe** from [Releases](https://github.com/ilunya100000/IlunyaBrowser/releases/latest) and run it.

Build from source:

```bat
run.bat
build.bat
```

## Linux

### Arch Linux (yay)

```bash
yay -S ilunyabrowser
```

- AUR: https://aur.archlinux.org/packages/ilunyabrowser
- AUR mirror (PKGBUILD): https://github.com/ilunya100000/ilunyabrowser-aur

If the package is not in AUR yet, install from the mirror:

```bash
git clone https://github.com/ilunya100000/ilunyabrowser-aur.git
cd ilunyabrowser-aur
makepkg -si
```

Or from this repository:

```bash
yay -S ./packaging/arch
```

### Debian / Ubuntu

Download **ilunyabrowser_1.0.1-1_all.deb** from [Releases](https://github.com/ilunya100000/IlunyaBrowser/releases/latest) and install:

```bash
sudo apt install ./ilunyabrowser_1.0.1-1_all.deb
```

Build from source:

```bash
sudo apt install build-essential debhelper python3-pyqt6 python3-pyqt6.qtwebengine
./packaging/debian/build-deb.sh
sudo apt install ../ilunyabrowser_1.0.1-1_all.deb
```

### Fedora / RHEL / Rocky / AlmaLinux

```bash
./packaging/rpm/build-rpm.sh
sudo dnf install packaging/rpmbuild/RPMS/noarch/ilunyabrowser-*.rpm
```

### Gentoo

```bash
./packaging/gentoo/prepare-overlay.sh
sudo eselect repository add ilunyabrowser packaging/gentoo-overlay/ilunyabrowser
sudo emerge --sync ilunyabrowser
sudo emerge -av www-client/ilunyabrowser
```

More details: [`packaging/INSTALL`](packaging/INSTALL)

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-linux.txt   # or requirements.txt on Windows
python ilunya_browser.py
```

## License

MIT
