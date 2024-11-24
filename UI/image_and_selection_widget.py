import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QPushButton, QFileDialog, 
                           QScrollArea, QSlider, QLabel, QApplication)
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen, QPolygon
from config.image_and_selection_widget_settings import *


# Use mouse to select a rectangle or lasso region
class SelectableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selection_polygon = QPolygon()
        self.start_point = QPoint()
        self.is_selecting = False
        self.mode = RECT_MODE  # Default mode is rectangle

    def toggleMode(self):
        # Toggle between rectangle and lasso modes
        self.mode = LASSO_MODE if self.mode == RECT_MODE else RECT_MODE

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_selecting = True
            self.start_point = event.pos()
            self.selection_polygon = QPolygon()
            self.selection_polygon.append(self.start_point)
            self.update()

    def mouseMoveEvent(self, event):
        if self.is_selecting:
            if self.mode == RECT_MODE:
                # Calculate the rectangle points based on start and current points
                current_point = event.pos()
                self.selection_polygon = QPolygon([
                    self.start_point,
                    QPoint(current_point.x(), self.start_point.y()),
                    current_point,
                    QPoint(self.start_point.x(), current_point.y())
                ])
            elif self.mode == LASSO_MODE:
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
            pen_color = QColor(*SELECTION_PEN_COLOR)
            painter.setPen(QPen(pen_color, SELECTION_PEN_WIDTH, Qt.SolidLine))
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
        self._imageHistory = []  # Store history images
        self._redoHistory = []   # Store redo history
        self._initUI()
        self.show()

    def _initUI(self):
        layout = QVBoxLayout()  # Main layout: vertical

        # Scrollable image area
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.label = SelectableLabel(self)
        self.scrollArea.setWidget(self.label)
        layout.addWidget(self.scrollArea)

        # Control buttons
        self.openImageButton = QPushButton(OPEN_BUTTON_TEXT, self)
        self.openImageButton.clicked.connect(self._openImage)
        layout.addWidget(self.openImageButton)

        self.saveButton = QPushButton(SAVE_BUTTON_TEXT, self)
        self.saveButton.clicked.connect(self._saveImage)
        layout.addWidget(self.saveButton)

        self.undoButton = QPushButton(UNDO_BUTTON_TEXT, self)
        self.undoButton.clicked.connect(self._undo)
        layout.addWidget(self.undoButton)

        self.redoButton = QPushButton(REDO_BUTTON_TEXT, self)
        self.redoButton.clicked.connect(self._redo)
        layout.addWidget(self.redoButton)

        self.toggleSelectionModeButton = QPushButton(
            TOGGLE_MODE_TEXT.format(self.label.mode), 
            self
        )
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
        imagePath, _ = QFileDialog.getOpenFileName(
            self, 
            OPEN_DIALOG_TITLE, 
            "", 
            IMAGE_FILTER
        )
        if imagePath:
            pixmap = QPixmap(imagePath)
            self.setImage(pixmap)

    def _saveImage(self):
        if self.label.pixmap():
            filePath, _ = QFileDialog.getSaveFileName(
                self, 
                SAVE_DIALOG_TITLE, 
                "", 
                SAVE_FILTERS
            )
            if filePath:
                self.label.pixmap().save(filePath)

    def _toggleSelectionMode(self):
        self.label.toggleMode()
        self.toggleSelectionModeButton.setText(
            TOGGLE_MODE_TEXT.format(self.label.mode)
        )

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