#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

if ! command -v yay >/dev/null 2>&1; then
  echo "yay is not installed. Install it first, for example:"
  echo "  sudo pacman -S --needed git base-devel"
  echo "  git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si"
  exit 1
fi

echo "Installing IlunyaBrowser via yay..."
echo "AUR: https://aur.archlinux.org/packages/ilunyabrowser"
echo
yay -S --needed --noconfirm ilunyabrowser 2>/dev/null || yay -S --needed --noconfirm "${ROOT}/packaging/arch"
