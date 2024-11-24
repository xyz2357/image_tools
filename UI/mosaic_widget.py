import sys
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from utils.image_utils import pixmap_to_pil_image_with_alpha, pil_image_to_qimage_with_alpha, apply_mosaic


class MosaicWidget(QWidget):
    def __init__(self, image_and_selection_source):
        super().__init__()
        self.mosaicSize = 15  # init mosaic size
        self.image_and_selection_source = image_and_selection_source
        self._initUI()

    def _initUI(self):
        layout = QVBoxLayout()

        # apply button
        self.applyMosaicButton = QPushButton("Apply Mosaic", self)
        self.applyMosaicButton.clicked.connect(self.applyMosaic)
        layout.addWidget(self.applyMosaicButton)
        self.applyMosaicButton.setFixedHeight(100)

        # label for mosaic size
        self.sizeLabel = QLabel(f"Mosaic Size: {self.mosaicSize}", self)
        layout.addWidget(self.sizeLabel)

        # slider for mosaic size
        self.sizeSlider = QSlider(Qt.Horizontal, self)
        self.sizeSlider.setMinimum(1)
        self.sizeSlider.setMaximum(8)
        self.sizeSlider.setValue(self.mosaicSize // 5)
        self.sizeSlider.valueChanged.connect(self._changeMosaicSize)
        layout.addWidget(self.sizeSlider)

        self.setLayout(layout)
        self.setMaximumHeight(200)

    def applyMosaic(self):
        pixmap = self.image_and_selection_source.getImage()
        selection_polygon = self.image_and_selection_source.getSelectionPolygon()

        if pixmap and len(selection_polygon) > 0:
            pil_image = pixmap_to_pil_image_with_alpha(pixmap)
            apply_mosaic(pil_image, selection_polygon, self.mosaicSize)
            # convert PIL Image back to QImage
            result_pixmap = pil_image_to_qimage_with_alpha(pil_image)
            self.image_and_selection_source.setImage(QPixmap.fromImage(result_pixmap))

    def _changeMosaicSize(self, value):
        self.mosaicSize = value * 5
        self.sizeLabel.setText(f"Mosaic Size: {self.mosaicSize}")