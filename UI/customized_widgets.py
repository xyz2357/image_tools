from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QRect, QPoint, Qt
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QLabel

# Use mouse to select a rectangle region
# TODO: add click small region to cancel selection
# TODO: sometimes the region will be cancelled if operate very quick
class SelectableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selection_rect = QRect()
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.is_selecting = False

    def mousePressEvent(self, event):
        self.start_point = event.pos()
        self.end_point = self.start_point
        self.is_selecting = True
        self.update()

    def mouseMoveEvent(self, event):
        if self.is_selecting:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        self.is_selecting = False
        # can add event here

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.is_selecting:
            painter = QPainter(self)
            painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.SolidLine))  # TODO: color and stroke size setting
            self.selection_rect = QRect(self.start_point, self.end_point)  # TODO: other shapes?
            painter.drawRect(self.selection_rect.normalized())


# TODO: signal