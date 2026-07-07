#!/usr/bin/env python3
"""Generate IlunyaBrowser icon (letter I on blue background)."""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
ICON_PATH = ASSETS_DIR / "icon.ico"
PNG_PATH = ASSETS_DIR / "icon.png"


def build_icon_pixmap(size: int) -> QPixmap:
    pixmap = QPixmap(size, size)
    pixmap.fill(QColor("#3B5BDB"))

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(QColor("#FFFFFF"))
    font = QFont()
    font.setFamilies(["Sans Serif", "DejaVu Sans", "Segoe UI"])
    font.setPixelSize(int(size * 0.62))
    font.setWeight(QFont.Weight.Bold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "I")
    painter.end()
    return pixmap


def make_app_icon() -> QIcon:
    icon = QIcon()
    for size in (16, 32, 48, 64, 128, 256):
        icon.addPixmap(build_icon_pixmap(size))
    return icon


def save_icon_files() -> Path:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    pixmap = build_icon_pixmap(256)
    pixmap.save(str(PNG_PATH), "PNG")
    pixmap.save(str(ICON_PATH), "ICO")
    return ICON_PATH


def main() -> None:
    app = QApplication([])
    path = save_icon_files()
    print(f"Icon saved: {path}")


if __name__ == "__main__":
    main()
