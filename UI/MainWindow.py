import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTabWidget

from UI.ImageAndSelectionWidget import ImageAndSelectionWidget
from UI.MosaicWidget import MosaicWidget


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

        self.mainLayout = QHBoxLayout()
        self.centralWidget.setLayout(self.mainLayout)

        self.imageAndSelectionWidget = ImageAndSelectionWidget()
        self.mainLayout.addWidget(self.imageAndSelectionWidget)

        self.tabs = QTabWidget()
        self.mainLayout.addWidget(self.tabs)
        self.tabs.setFixedWidth(400)

        self.mosaicWidget = MosaicWidget(self.imageAndSelectionWidget)
        self.tabs.addTab(self.mosaicWidget, "Add Mosaic")


def runMainWindow():
    app = QApplication(sys.argv)
    ex = ImageTool()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    runMainWindow()