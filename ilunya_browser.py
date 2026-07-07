#!/usr/bin/env python3
"""IlunyaBrowser — minimal Chromium-based browser with low RAM usage."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Callable, Optional
from urllib.parse import quote_plus

from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

APP_NAME = "IlunyaBrowser"
APP_ID = "IlunyaBrowser.App.1"
BASE_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
ASSETS_DIR = BASE_DIR / "assets"
ICON_CANDIDATES = (
    ASSETS_DIR / "icon.png",
    ASSETS_DIR / "icon.ico",
)
GOOGLE_HOME = "https://www.google.com"
GOOGLE_SEARCH = "https://www.google.com/search?q={query}"


def set_windows_app_identity() -> None:
    if sys.platform != "win32":
        return
    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)
    except Exception:
        pass


def load_app_icon() -> QIcon:
    for icon_path in ICON_CANDIDATES:
        if icon_path.is_file():
            return QIcon(str(icon_path))
    from make_icon import make_app_icon

    return make_app_icon()


class AddressBar(QLineEdit):
    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.returnPressed.emit()
            event.accept()
            return
        super().keyPressEvent(event)


def make_profile() -> QWebEngineProfile:
    profile = QWebEngineProfile(APP_NAME, None)
    profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
    profile.setHttpCacheMaximumSize(32 * 1024 * 1024)
    profile.setPersistentCookiesPolicy(
        QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies
    )
    return profile


def tune_settings(settings: QWebEngineSettings) -> None:
    settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, False)
    settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False)
    settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
    settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, False)
    settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, False)
    settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadIconsForPage, False)
    settings.setAttribute(QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, False)
    settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, False)
    settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, False)
    settings.setAttribute(QWebEngineSettings.WebAttribute.ScreenCaptureEnabled, False)
    settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, False)
    settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, False)


class BrowserTab(QWidget):
    def __init__(self, profile: QWebEngineProfile, url: str = GOOGLE_HOME, parent=None):
        super().__init__(parent)
        self._profile = profile
        self._signals_bound = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.placeholder = QWidget(self)
        self.placeholder.setStyleSheet("background: #202124;")
        layout.addWidget(self.placeholder)

        self.view: Optional[QWebEngineView] = None
        self._pending_url = url

    def ensure_view(self) -> QWebEngineView:
        if self.view is not None:
            return self.view

        self.view = QWebEngineView(self)
        tune_settings(self.view.settings())
        self.view.setPage(QWebEnginePage(self._profile, self.view))
        self.view.setUrl(QUrl(self._pending_url))

        layout = self.layout()
        layout.replaceWidget(self.placeholder, self.view)
        self.placeholder.deleteLater()
        self.placeholder = None  # type: ignore[assignment]
        return self.view

    def bind_signals(
        self,
        on_title: Callable[[str], None],
        on_url: Callable[[QUrl], None],
        on_load_finished: Callable[[], None],
    ) -> None:
        if self.view is None or self._signals_bound:
            return
        self.view.titleChanged.connect(on_title)
        self.view.urlChanged.connect(on_url)
        self.view.loadFinished.connect(lambda _ok: on_load_finished())
        self._signals_bound = True

    def unload_view(self) -> None:
        if self.view is None:
            return

        self._pending_url = self.view.url().toString() or self._pending_url
        layout = self.layout()
        self.placeholder = QWidget(self)
        self.placeholder.setStyleSheet("background: #202124;")
        layout.replaceWidget(self.view, self.placeholder)
        self.view.setParent(None)
        self.view.deleteLater()
        self.view = None
        self._signals_bound = False

    @property
    def current_url(self) -> str:
        if self.view is not None:
            return self.view.url().toString() or self._pending_url
        return self._pending_url

    @property
    def current_title(self) -> str:
        if self.view is not None:
            return self.view.title() or "Вкладка"
        return "Новая вкладка"


class MainWindow(QMainWindow):
    def __init__(self, app_icon: QIcon):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(app_icon)
        self.resize(1100, 720)
        self._profile = make_profile()

        central = QWidget(self)
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(4)

        nav = QHBoxLayout()
        nav.setSpacing(4)

        self.back_btn = QPushButton("←")
        self.forward_btn = QPushButton("→")
        self.reload_btn = QPushButton("↻")
        self.home_btn = QPushButton("⌂")
        for btn in (self.back_btn, self.forward_btn, self.reload_btn, self.home_btn):
            btn.setFixedWidth(34)
            nav.addWidget(btn)

        self.address_bar = AddressBar()
        self.address_bar.setPlaceholderText("Поиск в Google или введите адрес")
        nav.addWidget(self.address_bar, stretch=1)

        self.go_btn = QPushButton("→")
        self.go_btn.setFixedWidth(34)
        self.go_btn.setToolTip("Открыть")
        nav.addWidget(self.go_btn)

        root.addLayout(nav)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)

        self.new_tab_btn = QPushButton("+")
        self.new_tab_btn.setFixedSize(30, 24)
        self.new_tab_btn.setToolTip("Новая вкладка")
        self.new_tab_btn.clicked.connect(self._new_tab_shortcut)
        self.tabs.setCornerWidget(self.new_tab_btn, Qt.Corner.TopRightCorner)

        root.addWidget(self.tabs, stretch=1)

        self.back_btn.clicked.connect(self._go_back)
        self.forward_btn.clicked.connect(self._go_forward)
        self.reload_btn.clicked.connect(self._reload)
        self.home_btn.clicked.connect(self._go_home)
        self.go_btn.clicked.connect(self._navigate_from_bar)
        self.address_bar.returnPressed.connect(self._navigate_from_bar)
        self.tabs.tabCloseRequested.connect(self._close_tab)
        self.tabs.currentChanged.connect(self._on_tab_changed)

        self._wire_shortcuts()
        self.new_tab(GOOGLE_HOME)

    def _wire_shortcuts(self) -> None:
        shortcuts = (
            (QKeySequence("Ctrl+T"), self._new_tab_shortcut),
            (QKeySequence("Ctrl+W"), self._close_current_tab),
            (QKeySequence("Ctrl+L"), self.address_bar.setFocus),
            (QKeySequence("F5"), self._reload),
        )
        for sequence, handler in shortcuts:
            action = QAction(self)
            action.setShortcut(sequence)
            action.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
            action.triggered.connect(handler)
            self.addAction(action)

    def _active_tab(self) -> Optional[BrowserTab]:
        widget = self.tabs.currentWidget()
        return widget if isinstance(widget, BrowserTab) else None

    def _active_view(self) -> Optional[QWebEngineView]:
        tab = self._active_tab()
        return tab.ensure_view() if tab else None

    def new_tab(self, url: str = GOOGLE_HOME) -> None:
        tab = BrowserTab(self._profile, url, self)
        index = self.tabs.addTab(tab, "Новая вкладка")
        self.tabs.setCurrentIndex(index)
        self._activate_tab(tab)

    def _activate_tab(self, tab: BrowserTab) -> None:
        tab.ensure_view()
        tab.bind_signals(
            lambda title, t=tab: self._on_title_changed(t, title),
            lambda qurl, t=tab: self._on_url_changed(t, qurl),
            lambda t=tab: self._sync_address_bar(t),
        )
        self._sync_address_bar(tab)

    def _on_title_changed(self, tab: BrowserTab, title: str) -> None:
        index = self.tabs.indexOf(tab)
        if index >= 0:
            self.tabs.setTabText(index, (title or "Вкладка")[:28])

    def _on_url_changed(self, tab: BrowserTab, url: QUrl) -> None:
        if self.tabs.currentWidget() is tab:
            self.address_bar.setText(url.toString())

    def _sync_address_bar(self, tab: BrowserTab) -> None:
        if self.tabs.currentWidget() is tab:
            self.address_bar.setText(tab.current_url)

    def _on_tab_changed(self, index: int) -> None:
        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            if not isinstance(widget, BrowserTab):
                continue
            if i == index:
                self._activate_tab(widget)
            else:
                widget.unload_view()

    def _close_tab(self, index: int) -> None:
        if self.tabs.count() <= 1:
            self.close()
            return
        widget = self.tabs.widget(index)
        self.tabs.removeTab(index)
        if widget is not None:
            widget.deleteLater()

    def _close_current_tab(self) -> None:
        self._close_tab(self.tabs.currentIndex())

    def _new_tab_shortcut(self) -> None:
        self.new_tab(GOOGLE_HOME)

    @staticmethod
    def _normalize_input(text: str) -> str:
        value = text.strip()
        if not value:
            return GOOGLE_HOME
        if " " in value and "." not in value and not value.startswith(("http://", "https://")):
            return GOOGLE_SEARCH.format(query=quote_plus(value))
        if "." not in value and not value.startswith(("http://", "https://", "localhost")):
            return GOOGLE_SEARCH.format(query=quote_plus(value))
        if not value.startswith(("http://", "https://")):
            return f"https://{value}"
        return value

    def _navigate_from_bar(self) -> None:
        tab = self._active_tab()
        if tab is None:
            return
        url = self._normalize_input(self.address_bar.text())
        view = tab.ensure_view()
        view.setUrl(QUrl(url))
        view.setFocus()

    def _go_back(self) -> None:
        view = self._active_view()
        if view:
            view.back()

    def _go_forward(self) -> None:
        view = self._active_view()
        if view:
            view.forward()

    def _reload(self) -> None:
        view = self._active_view()
        if view:
            view.reload()

    def _go_home(self) -> None:
        tab = self._active_tab()
        if tab:
            tab.ensure_view().setUrl(QUrl(GOOGLE_HOME))


def configure_app(app: QApplication, app_icon: QIcon) -> None:
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_NAME)
    app.setOrganizationName(APP_NAME)
    app.setDesktopFileName(APP_NAME)
    app.setWindowIcon(app_icon)
    app.setStyle("Fusion")


def apply_chromium_flags() -> None:
    flags = [
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--disable-extensions",
        "--disable-background-networking",
        "--disable-sync",
        "--disable-default-apps",
        "--disable-translate",
        "--disable-component-update",
        "--no-default-browser-check",
        "--disable-features=Translate,MediaRouter,OptimizationHints,AutofillServerCommunication",
    ]
    existing = os.environ.get("QTWEBENGINE_CHROMIUM_FLAGS", "").strip()
    merged = f"{existing} {' '.join(flags)}".strip()
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = merged


def main() -> int:
    apply_chromium_flags()
    set_windows_app_identity()
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    app_icon = load_app_icon()
    configure_app(app, app_icon)

    window = MainWindow(app_icon)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
