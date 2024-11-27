from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QSlider, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from utils.image_utils import (
    pixmap_to_pil_image_with_alpha, 
    pil_image_to_qimage_with_alpha, 
    add_camera_effect
)
from config.settings import Settings

class CameraWidget(QWidget):
    def __init__(self, image_and_selection_source):
        super().__init__()
        self.batteryLevel = Settings.Camera.BATTERY_LEVEL['DEFAULT']
        self.timerText = Settings.Camera.TIMER_TEXT['DEFAULT']
        self.image_and_selection_source = image_and_selection_source
        self._initUI()

    def _initUI(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)
        
        # Battery level label
        self.batteryLabel = QLabel(Settings.Camera.BATTERY_LABEL_TEXT.format(self.batteryLevel), self)
        self.batteryLabel.setFixedHeight(Settings.Common.Sizes.LABEL_HEIGHT)
        layout.addWidget(self.batteryLabel)

        # Battery level slider
        self.batterySlider = QSlider(Qt.Horizontal, self)
        self.batterySlider.setMinimum(Settings.Camera.BATTERY_LEVEL['MIN'])
        self.batterySlider.setMaximum(Settings.Camera.BATTERY_LEVEL['MAX'])
        self.batterySlider.setValue(int(self.batteryLevel * 100))  # Assuming slider is 0-100    
        self.batterySlider.valueChanged.connect(self._changeBatteryLevel)
        self.batterySlider.setFixedHeight(Settings.Common.Sizes.SLIDER_HEIGHT)
        layout.addWidget(self.batterySlider)

        # Timer input
        self.timerInput = QLineEdit(self)
        self.timerInput.setText(self.timerText)
        self.timerInput.setFixedHeight(Settings.Common.Sizes.INPUT_HEIGHT)
        layout.addWidget(self.timerInput)

        # Apply camera effect button
        self.applyCameraEffectButton = QPushButton(
            Settings.get_button_text_with_shortcut(Settings.ButtonText.Tools.APPLY_CAMERA_EFFECT),
            self
        )
        self.applyCameraEffectButton.clicked.connect(self.applyCameraEffect)
        self.applyCameraEffectButton.setFixedHeight(Settings.Common.Sizes.BUTTON_HEIGHT)
        layout.addWidget(self.applyCameraEffectButton)

        self.setLayout(layout)

    def _changeBatteryLevel(self, value):
        """Update battery level based on slider value"""
        self.batteryLevel = value / 100.0  # Convert slider value to 0-1 range
        self.batteryLabel.setText(Settings.Camera.BATTERY_LABEL_TEXT.format(self.batteryLevel))

    def applyCameraEffect(self):
        """Apply camera effect to the image"""
        pixmap = self.image_and_selection_source.getImage()

        if pixmap:
            # Convert QPixmap to PIL Image
            pil_image = pixmap_to_pil_image_with_alpha(pixmap)
            
            # Apply camera effect
            add_camera_effect(pil_image, self.batteryLevel, self.timerInput.text())
            
            # Convert back to QPixmap and update image
            result_pixmap = pil_image_to_qimage_with_alpha(pil_image)
            self.image_and_selection_source.setImage(QPixmap.fromImage(result_pixmap)) 