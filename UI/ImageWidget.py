from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QFileDialog, QScrollArea, QSlider
from PyQt5.QtGui import QPixmap
from UI.customized_widgets import SelectableLabel

# A main image widget to open, undo and save widget
# TODO: redo
# TODO: zooming?
# TODO: connect signal here
class ImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._imageHistory = []  # store history images
        self._initUI()
        self.show()  # TODO: if inherit, not show

    def _initUI(self):
        layout = QVBoxLayout()  # main layout: vertical

        # A QScrollArea to show image
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.label = SelectableLabel(self)
        self.scrollArea.setWidget(self.label)
        layout.addWidget(self.scrollArea)

        # A button to open image
        self.openImageButton = QPushButton("Open Image", self)
        self.openImageButton.clicked.connect(self._openImage)
        layout.addWidget(self.openImageButton)

        # Ad button to save image
        self.saveButton = QPushButton("Save Image", self)
        self.saveButton.clicked.connect(self._saveImage)
        layout.addWidget(self.saveButton)

        # A button to undo
        self.undoButton = QPushButton("Undo", self)
        self.undoButton.clicked.connect(self._undo)
        layout.addWidget(self.undoButton)

        self.setLayout(layout)

    def _undo(self):
        if self._imageHistory:
            # pop history state
            previous_pixmap = self._imageHistory.pop()
            self.label.setPixmap(previous_pixmap)

    def _addToUndo(self):
        if self.label.pixmap():
            self._imageHistory.append(self.label.pixmap().copy())

    def _openImage(self):
        imagePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
        if imagePath:
            pixmap = QPixmap(imagePath)
            self.setImage(pixmap)

    def _saveImage(self):
        # TODO: (1) default name, (2) default format
        if self.label.pixmap():
            filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "JPG Files (*.jpg *.jpeg);;PNG Files (*.png);;All Files (*)")
            if filePath:
                self.label.pixmap().save(filePath)
 
    def getImage(self):
        return self.label.pixmap()
    
    def setImage(self, pixmap):
        self._addToUndo()
        self.label.setPixmap(pixmap)
        self.label.adjustSize()  # adjust UI size to fit image  # TODO: shall we?