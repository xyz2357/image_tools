import sys
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from utils.image_utils import (
    pixmap_to_pil_image_with_alpha, 
    pil_image_to_qimage_with_alpha, 
    apply_mosaic
)
from config.mosaic_widget_settings import *


class MosaicWidget(QWidget):
    def __init__(self, image_and_selection_source):
        super().__init__()
        self.mosaicSize = MOSAIC_SIZE_DEFAULT
        self.image_and_selection_source = image_and_selection_source
        self._initUI()

    def _initUI(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()

        # Apply mosaic button
        self.applyMosaicButton = QPushButton(APPLY_BUTTON_TEXT, self)
        self.applyMosaicButton.clicked.connect(self.applyMosaic)
        self.applyMosaicButton.setFixedHeight(BUTTON_HEIGHT)
        layout.addWidget(self.applyMosaicButton)

        # Mosaic size label
        self.sizeLabel = QLabel(SIZE_LABEL_TEXT.format(self.mosaicSize), self)
        layout.addWidget(self.sizeLabel)

        # Mosaic size slider
        self.sizeSlider = QSlider(Qt.Horizontal, self)
        self.sizeSlider.setMinimum(MOSAIC_SIZE_MIN)
        self.sizeSlider.setMaximum(MOSAIC_SIZE_MAX)
        self.sizeSlider.setValue(self.mosaicSize // MOSAIC_SIZE_MULTIPLIER)
        self.sizeSlider.valueChanged.connect(self._changeMosaicSize)
        layout.addWidget(self.sizeSlider)

        self.setLayout(layout)
        self.setMaximumHeight(WIDGET_MAX_HEIGHT)

    def applyMosaic(self):
        """Apply mosaic effect to the selected area"""
        pixmap = self.image_and_selection_source.getImage()
        selection_polygon = self.image_and_selection_source.getSelectionPolygon()

        if pixmap and len(selection_polygon) > 0:
            # Convert QPixmap to PIL Image
            pil_image = pixmap_to_pil_image_with_alpha(pixmap)
            
            # Apply mosaic effect
            apply_mosaic(pil_image, selection_polygon, self.mosaicSize)
            
            # Convert back to QPixmap and update image
            result_pixmap = pil_image_to_qimage_with_alpha(pil_image)
            self.image_and_selection_source.setImage(QPixmap.fromImage(result_pixmap))

    def _changeMosaicSize(self, value):
        """Update mosaic size based on slider value"""
        self.mosaicSize = value * MOSAIC_SIZE_MULTIPLIER
        self.sizeLabel.setText(SIZE_LABEL_TEXT.format(self.mosaicSize))