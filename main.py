import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget

class CombinedApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create the tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Set window properties
        self.setWindowTitle('Image Tools')
        self.setGeometry(200, 200, 1024, 768)

def main():
    app = QApplication(sys.argv)
    ex = CombinedApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()