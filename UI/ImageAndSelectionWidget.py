from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QFileDialog, QScrollArea, QSlider
from PyQt5.QtGui import QPixmap
from UI.SelectableLabel import SelectableLabel

# A main image widget to open, undo and save widget
# TODO: zooming?
# TODO: connect signal here
class ImageAndSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._imageHistory = []  # store history images
        self._redoHistory = []   # store redo history
        self._initUI()
        self.show()

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

        # Add redo button
        self.redoButton = QPushButton("Redo", self)
        self.redoButton.clicked.connect(self._redo)
        layout.addWidget(self.redoButton)

        self.toggleSelectionModeButton = QPushButton("ToggleSelectionMode (Current: %s)" %(self.label.mode), self)
        self.toggleSelectionModeButton.clicked.connect(self._toggleSelectionMode)
        layout.addWidget(self.toggleSelectionModeButton)

        self.setLayout(layout)

    def _undo(self):
        if self._imageHistory:
            if self.label.pixmap():
                self._redoHistory.append(self.label.pixmap().copy())
            previous_pixmap = self._imageHistory.pop()
            self.label.setPixmap(previous_pixmap)

    def _redo(self):
        if self._redoHistory:
            if self.label.pixmap():
                self._imageHistory.append(self.label.pixmap().copy())
            next_pixmap = self._redoHistory.pop()
            self.label.setPixmap(next_pixmap)

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

    def _toggleSelectionMode(self):
        self.label.toggleMode()
        self.toggleSelectionModeButton.setText("ToggleSelectionMode (Current: %s)" %(self.label.mode))
 
    def getImage(self):
        return self.label.pixmap()
    
    def setImage(self, pixmap):
        self._addToUndo()
        self._redoHistory.clear()  # clear redo history when new image is set
        self.label.setPixmap(pixmap)
        self.label.adjustSize()

    def getSelectionPolygon(self, to_points=True):
        if not to_points:
            return self.label.selection_polygon
        return [(p.x(), p.y()) for p in self.label.selection_polygon]