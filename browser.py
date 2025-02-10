import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QHBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QIcon

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window properties
        self.setWindowTitle("My Web Browser")
        self.setGeometry(100, 100, 1200, 800)

        # Create the web view widget
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        # Create navigation buttons
        self.back_button = QPushButton("←")
        self.back_button.clicked.connect(self.browser.back)

        self.forward_button = QPushButton("→")
        self.forward_button.clicked.connect(self.browser.forward)

        self.reload_button = QPushButton("⟳")
        self.reload_button.clicked.connect(self.browser.reload)

        self.home_button = QPushButton("🏠")
        self.home_button.clicked.connect(self.go_home)

        # Create URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate)

        # Connect browser's URL changed signal to update URL bar
        self.browser.urlChanged.connect(self.update_url)

        # Create a horizontal layout for navigation buttons
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.reload_button)
        nav_layout.addWidget(self.home_button)

        # Create the main layout
        layout = QVBoxLayout()
        layout.addWidget(self.url_bar)
        layout.addLayout(nav_layout)
        layout.addWidget(self.browser)

        # Create a central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def navigate(self):
        """
        Navigate to the URL entered in the URL bar.
        Automatically adds 'https://' if no protocol is specified.
        """
        url = self.url_bar.text()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        # Use QUrl for proper URL handling
        self.browser.setUrl(QUrl(url))

    def update_url(self, url):
        """
        Update the URL bar with the current page's URL.
        """
        self.url_bar.setText(url.toString())

    def go_home(self):
        """
        Navigate to the home page (Google in this example).
        """
        self.browser.setUrl(QUrl("https://www.google.com"))

def main():
    """
    Main function to set up and run the application.
    """
    app = QApplication(sys.argv)
    
    # Optional: Set application-wide icon
    app.setWindowIcon(QIcon.fromTheme("web-browser"))
    
    window = Browser()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()