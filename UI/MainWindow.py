import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from UI.ImageWidget import ImageWidget


class ImageTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle('Image Tools')
        self.setGeometry(200, 200, 1024, 768)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QVBoxLayout()  # main layout: vertical
        self.centralWidget.setLayout(self.mainLayout)

        self.imageWidget = ImageWidget()
        self.mainLayout.addWidget(self.imageWidget)


def runMainWindow():
    app = QApplication(sys.argv)
    ex = ImageTool()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    runMainWindow()