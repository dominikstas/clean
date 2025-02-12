import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                             QPushButton, QLineEdit, QHBoxLayout, QMessageBox,
                             QProgressBar)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from PyQt6.QtCore import QUrl, Qt, QSize
from PyQt6.QtGui import QKeySequence, QAction, QIcon

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window settings
        self.setWindowTitle("Modern Browser")
        self.setGeometry(100, 100, 1200, 800)

        # Create browser view
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.browser.urlChanged.connect(self.update_url)
        self.browser.loadStarted.connect(self.load_started)
        self.browser.loadProgress.connect(self.update_progress)
        self.browser.loadFinished.connect(self.load_finished)

        # Enable JavaScript and other settings
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)

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

        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        self.browser.setUrl(QUrl(url))

    def update_url(self, url):
        self.url_bar.setText(url.toString())

    def go_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def load_started(self):
        self.progress_bar.setValue(0)
        self.progress_bar.show()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def load_finished(self, ok):
        self.progress_bar.hide()
        if not ok:
            self.show_error_message("Failed to load the page")

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
    app = QApplication(sys.argv)
    app.setApplicationName("Modern Browser")
    app.setStyle("Fusion")  # Use Fusion style for a more modern look
    
    window = Browser()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()