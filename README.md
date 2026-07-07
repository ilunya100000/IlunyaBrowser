# IlunyaBrowser

Minimal Chromium-based browser (Qt WebEngine) focused on low RAM usage.

Features:
- Google homepage and search
- Multiple tabs with inactive tab unloading
- No bookmarks, extensions, sync, or other bloat

## Windows

Download **IlunyaBrowser.exe** from [Releases](https://github.com/ilunya100000/IlunyaBrowser/releases/latest) and run it.

Or build from source:

```bat
run.bat
build.bat
```

## Linux

### Arch Linux (yay)

After the package is published to AUR:

```bash
yay -S ilunyabrowser
```

From this repository before AUR publish:

```bash
yay -S ./packaging/arch
```

AUR package files: [`packaging/aur/`](packaging/aur/)

### Debian / Ubuntu

```bash
./packaging/debian/build-deb.sh
sudo apt install ../ilunyabrowser_1.0.0-1_all.deb
```

### Fedora / RHEL

```bash
./packaging/rpm/build-rpm.sh
sudo dnf install packaging/rpmbuild/RPMS/noarch/ilunyabrowser-*.rpm
```

### Gentoo

```bash
./packaging/gentoo/prepare-overlay.sh
sudo eselect repository add ilunyabrowser packaging/gentoo-overlay/ilunyabrowser
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
