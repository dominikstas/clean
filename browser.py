import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                             QPushButton, QLineEdit, QHBoxLayout, QMessageBox,
                             QProgressBar)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage, QWebEngineProfile
from PyQt6.QtCore import QUrl, Qt, QSize
from PyQt6.QtGui import QKeySequence, QAction, QIcon

class CustomWebPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"Console: {message} at line {lineNumber} from {sourceID}")

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Enable debug logging
        os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--enable-logging --log-level=0'
        
        # Main window settings
        self.setWindowTitle("Modern Browser")
        self.setGeometry(100, 100, 1200, 800)

        # Create and configure web profile
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
        
        # Ensure the storage path exists
        storage_path = "./browser_data"
        os.makedirs(storage_path, exist_ok=True)
        self.profile.setPersistentStoragePath(storage_path)
        
        # Create browser view with custom page
        self.browser = QWebEngineView()
        self.page = CustomWebPage(self.profile, self.browser)
        self.browser.setPage(self.page)
        
        # Enable JavaScript and other settings
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ErrorPageEnabled, True)

        # Connect signals for better error handling
        self.page.loadFinished.connect(self.handle_load_finished)
        self.page.loadStarted.connect(self.load_started)
        self.page.loadProgress.connect(self.update_progress)
        
        # Set initial URL
        self.navigate_to_url("https://www.google.com")

        # Address bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate)
        self.url_bar.setPlaceholderText("Enter URL")
        self.url_bar.setStyleSheet("""
            QLineEdit {
                border: 1px solid #555;
                border-radius: 10px;
                padding: 5px 15px;
                background: #2a2a2a;
                color: #fff;
            }
        """)

        # Navigation buttons
        self.back_button = self.create_nav_button("◀", self.browser.back, "Go back")
        self.forward_button = self.create_nav_button("▶", self.browser.forward, "Go forward")
        self.reload_button = self.create_nav_button("↻", self.browser.reload, "Reload page")
        self.home_button = self.create_nav_button("🏠", self.go_home, "Go home")

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background: #2a2a2a;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)

        # Layout
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.reload_button)
        nav_layout.addWidget(self.home_button)
        nav_layout.addWidget(self.url_bar)
        nav_layout.setSpacing(10)
        nav_layout.setContentsMargins(10, 10, 10, 0)

        main_layout = QVBoxLayout()
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.browser)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Main container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Shortcuts
        self.setup_shortcuts()

        # Apply dark theme
        self.apply_dark_theme()

    def navigate_to_url(self, url_string):
        url = QUrl(url_string)
        if url.scheme() == "":
            url.setScheme("https")
        self.browser.setUrl(url)
        print(f"Navigating to: {url.toString()}")

    def create_nav_button(self, text, connection, tooltip):
        button = QPushButton(text)
        button.clicked.connect(connection)
        button.setToolTip(tooltip)
        button.setStyleSheet("""
            QPushButton {
                background-color: #2a2a2a;
                color: #fff;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)
        return button

    def navigate(self):
        url = self.url_bar.text().strip()
        if not url:
            return
        self.navigate_to_url(url)

    def update_url(self, url):
        self.url_bar.setText(url.toString())

    def go_home(self):
        self.navigate_to_url("https://www.google.com")

    def load_started(self):
        print("Page load started")
        self.progress_bar.setValue(0)
        self.progress_bar.show()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)
        print(f"Loading progress: {progress}%")

    def handle_load_finished(self, ok):
        self.progress_bar.hide()
        if not ok:
            error_info = "Unknown error"
            if hasattr(self.page, 'error_info'):
                error_info = self.page.error_info
            self.show_error_message(f"Failed to load the page: {error_info}")
            print(f"Page load failed: {error_info}")
        else:
            print("Page loaded successfully")
            self.update_url(self.browser.url())

    def show_error_message(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Icon.Warning)
        error_box.setText(message)
        error_box.setWindowTitle("Error")
        error_box.exec()

    def setup_shortcuts(self):
        self.back_button.setShortcut(QKeySequence.StandardKey.Back)
        self.forward_button.setShortcut(QKeySequence.StandardKey.Forward)
        self.reload_button.setShortcut(QKeySequence.StandardKey.Refresh)
        self.url_bar.setClearButtonEnabled(True)

        refresh_action = QAction(self)
        refresh_action.setShortcut(QKeySequence(Qt.Key.Key_F5))
        refresh_action.triggered.connect(self.browser.reload)
        self.addAction(refresh_action)

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
            }
        """)

def main():
    # Enable debug flags
    os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = '9222'
    
    app = QApplication(sys.argv)
    app.setApplicationName("Modern Browser")
    app.setStyle("Fusion")
    
    window = Browser()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()