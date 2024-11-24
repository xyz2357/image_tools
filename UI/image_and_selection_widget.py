import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QFileDialog, QScrollArea, QSlider, QLabel, QApplication
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen, QPolygon


# Use mouse to select a rectangle or lasso region
class SelectableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selection_polygon = QPolygon()
        self.start_point = QPoint()
        self.is_selecting = False
        self.mode = "Rect"  # Default mode is rectangle

    def toggleMode(self):
        # Toggle between 'rect' and 'lasso'
        if self.mode == "Rect":
            self.mode = "Lasso"
        else:
            self.mode = "Rect"

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_selecting = True
            self.start_point = event.pos()
            self.selection_polygon = QPolygon()
            self.selection_polygon.append(self.start_point)
            self.update()

    def mouseMoveEvent(self, event):
        if self.is_selecting:
            if self.mode == "Rect":
                # Calculate the rectangle points based on start and current points
                current_point = event.pos()
                self.selection_polygon = QPolygon([
                    self.start_point,
                    QPoint(current_point.x(), self.start_point.y()),
                    current_point,
                    QPoint(self.start_point.x(), current_point.y())
                ])
            elif self.mode == "Lasso":
                # Append the current point to create a free-form selection
                self.selection_polygon.append(event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_selecting = False
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.selection_polygon.isEmpty():
            painter = QPainter(self)
            painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.SolidLine))
            painter.drawPolygon(self.selection_polygon)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SelectableLabel()
    window.setGeometry(100, 100, 800, 600)
    window.show()

    # Example: Toggle between modes (can be called from a button or any trigger)
    window.toggleMode()  # Switches to lasso mode
    window.toggleMode()  # Switches back to rectangle mode

    sys.exit(app.exec_())


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