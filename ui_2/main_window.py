import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTabWidget
from PyQt5.QtCore import Qt

from ui.image_and_selection_widget import ImageAndSelectionWidget
from ui.mosaic_widget import MosaicWidget
from ui.text_widget import TextWidget
from config.settings import Settings
from utils.shortcut_utils import create_shortcut


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initShortcuts()

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

    def initShortcuts(self):
        # File operations
        create_shortcut(
            self, 
            Settings.Shortcut.File.OPEN, 
            self.imageAndSelectionWidget._openImage
        )
        create_shortcut(
            self, 
            Settings.Shortcut.File.SAVE, 
            self.imageAndSelectionWidget._saveImage
        )

        # Edit operations
        create_shortcut(
            self, 
            Settings.Shortcut.Edit.UNDO, 
            self.imageAndSelectionWidget._undo
        )
        create_shortcut(
            self, 
            Settings.Shortcut.Edit.REDO, 
            self.imageAndSelectionWidget._redo
        )

        # Tool operations
        create_shortcut(
            self, 
            Settings.Shortcut.Edit.TOGGLE_SELECT, 
            self.imageAndSelectionWidget._toggleSelectionMode
        )
        create_shortcut(
            self, 
            Settings.Shortcut.Tools.APPLY_TEXT, 
            self.textWidget.applyText
        )
        create_shortcut(
            self, 
            Settings.Shortcut.Tools.APPLY_MOSAIC, 
            self.mosaicWidget.applyMosaic
        )


def runMainWindow():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    runMainWindow()