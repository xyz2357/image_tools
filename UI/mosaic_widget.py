from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from utils.image_utils import (
    pixmap_to_pil_image_with_alpha, 
    pil_image_to_qimage_with_alpha, 
    apply_mosaic
)
from config.settings import Settings


class MosaicWidget(QWidget):
    def __init__(self, image_and_selection_source):
        super().__init__()
        self.mosaicSize = Settings.Mosaic.MOSAIC_SIZE['DEFAULT']
        self.image_and_selection_source = image_and_selection_source
        self._initUI()

    def _initUI(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)
        
        # Mosaic size label
        self.sizeLabel = QLabel(Settings.Mosaic.SIZE_LABEL_TEXT.format(self.mosaicSize), self)
        self.sizeLabel.setFixedHeight(Settings.Common.Sizes.LABEL_HEIGHT)
        layout.addWidget(self.sizeLabel)

        # Mosaic size slider
        self.sizeSlider = QSlider(Qt.Horizontal, self)
        self.sizeSlider.setMinimum(Settings.Mosaic.MOSAIC_SIZE['MIN'])
        self.sizeSlider.setMaximum(Settings.Mosaic.MOSAIC_SIZE['MAX'])
        self.sizeSlider.setValue(self.mosaicSize // Settings.Mosaic.SIZE_MULTIPLIER)
        self.sizeSlider.valueChanged.connect(self._changeMosaicSize)
        self.sizeSlider.setFixedHeight(Settings.Common.Sizes.SLIDER_HEIGHT)
        layout.addWidget(self.sizeSlider)

        # Apply mosaic button
        self.applyMosaicButton = QPushButton(
            Settings.get_button_text_with_shortcut(Settings.ButtonText.Tools.APPLY_MOSAIC),
            self
        )
        self.applyMosaicButton.clicked.connect(self.applyMosaic)
        self.applyMosaicButton.setFixedHeight(Settings.Common.Sizes.BUTTON_HEIGHT)
        layout.addWidget(self.applyMosaicButton)

        self.setLayout(layout)

    def _changeMosaicSize(self, value):
        """Update mosaic size based on slider value"""
        self.mosaicSize = value * Settings.Mosaic.SIZE_MULTIPLIER
        self.sizeLabel.setText(Settings.Mosaic.SIZE_LABEL_TEXT.format(self.mosaicSize))

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