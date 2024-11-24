from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QPushButton, QFileDialog, 
                           QScrollArea, QSlider, QLabel, QApplication)
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen, QPolygon
from config.settings import Settings


# Use mouse to select a rectangle or lasso region
class SelectableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selection_polygon = QPolygon()
        self.start_point = QPoint()
        self.is_selecting = False
        self.mode = Settings.Image.Selection.MODES['RECT']  # Default mode is rectangle

    def toggleMode(self):
        # Toggle between rectangle and lasso modes
        self.mode = Settings.Image.Selection.MODES['LASSO'] if self.mode == Settings.Image.Selection.MODES['RECT'] else Settings.Image.Selection.MODES['RECT']

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_selecting = True
            self.start_point = event.pos()
            self.selection_polygon = QPolygon()
            self.selection_polygon.append(self.start_point)
            self.update()

    def mouseMoveEvent(self, event):
        if self.is_selecting:
            if self.mode == Settings.Image.Selection.MODES['RECT']:
                # Calculate the rectangle points based on start and current points
                current_point = event.pos()
                self.selection_polygon = QPolygon([
                    self.start_point,
                    QPoint(current_point.x(), self.start_point.y()),
                    current_point,
                    QPoint(self.start_point.x(), current_point.y())
                ])
            elif self.mode == Settings.Image.Selection.MODES['LASSO']:
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
            pen_color = QColor(*Settings.Image.Selection.PEN_COLOR)
            painter.setPen(QPen(pen_color, Settings.Image.Selection.PEN_WIDTH, Qt.SolidLine))
            painter.drawPolygon(self.selection_polygon)


# A main image widget to open, undo and save widget
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
        self.openImageButton = QPushButton(Settings.Image.Buttons.OPEN, self)
        self.openImageButton.clicked.connect(self._openImage)
        layout.addWidget(self.openImageButton)

        self.saveButton = QPushButton(Settings.Image.Buttons.SAVE, self)
        self.saveButton.clicked.connect(self._saveImage)
        layout.addWidget(self.saveButton)

        self.undoButton = QPushButton(Settings.Image.Buttons.UNDO, self)
        self.undoButton.clicked.connect(self._undo)
        layout.addWidget(self.undoButton)

        self.redoButton = QPushButton(Settings.Image.Buttons.REDO, self)
        self.redoButton.clicked.connect(self._redo)
        layout.addWidget(self.redoButton)

        self.toggleSelectionModeButton = QPushButton(
            Settings.Image.Buttons.TOGGLE_MODE.format(Settings.Image.Selection.MODES['RECT']), 
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
            Settings.Image.FileDialog.OPEN_TITLE, 
            "", 
            Settings.Image.FileDialog.IMAGE_FILTER
        )
        if imagePath:
            pixmap = QPixmap(imagePath)
            self.setImage(pixmap)

    def _saveImage(self):
        if self.label.pixmap():
            filePath, _ = QFileDialog.getSaveFileName(
                self, 
                Settings.Image.FileDialog.SAVE_TITLE, 
                "", 
                Settings.Image.FileDialog.SAVE_FILTER
            )
            if filePath:
                self.label.pixmap().save(filePath)

    def _toggleSelectionMode(self):
        self.label.toggleMode()
        self.toggleSelectionModeButton.setText(
            Settings.Image.Buttons.TOGGLE_MODE.format(Settings.Image.Selection.MODES[self.label.mode])
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