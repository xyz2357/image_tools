import sys
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QPolygon

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


# TODO: signal