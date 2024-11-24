import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTabWidget

from ui.image_and_selection_widget import ImageAndSelectionWidget
from ui.mosaic_widget import MosaicWidget
from ui.text_widget import TextWidget
from config.settings import Settings


class ImageTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle('Image Tools')
        self.setGeometry(Settings.Common.Sizes.MAIN_WINDOW_X, Settings.Common.Sizes.MAIN_WINDOW_Y, Settings.Common.Sizes.MAIN_WINDOW_WIDTH, Settings.Common.Sizes.MAIN_WINDOW_HEIGHT)

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

        self.textWidget = TextWidget(self.imageAndSelectionWidget)
        self.tabs.addTab(self.textWidget, "Add Text")


def runMainWindow():
    app = QApplication(sys.argv)
    ex = ImageTool()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    runMainWindow()