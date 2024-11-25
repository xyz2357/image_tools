from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QWidget, QPushButton, 
                           QSlider, QHBoxLayout, QSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen

from utils.image_utils import (
    pixmap_to_pil_image_with_alpha, 
    pil_image_to_qimage_with_alpha, 
    apply_optimized_motion_blur_to_polygon
)
from config.settings import Settings


class BlurWidget(QWidget):
    def __init__(self, image_and_selection_source):
        super().__init__()
        self.blur_intensity = Settings.Blur.INTENSITY['DEFAULT']
        self.blur_angle = Settings.Blur.ANGLE['DEFAULT']
        self.image_and_selection_source = image_and_selection_source
        self._initUI()

    def _initUI(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)
        
        # Blur intensity label
        self.intensityLabel = QLabel(Settings.Blur.INTENSITY_LABEL_TEXT.format(self.blur_intensity), self)
        self.intensityLabel.setFixedHeight(Settings.Common.Sizes.LABEL_HEIGHT)
        layout.addWidget(self.intensityLabel)

        # Blur intensity slider
        self.intensitySlider = QSlider(Qt.Horizontal, self)
        self.intensitySlider.setMinimum(Settings.Blur.INTENSITY['MIN'])
        self.intensitySlider.setMaximum(Settings.Blur.INTENSITY['MAX'])
        self.intensitySlider.setValue(self.blur_intensity)
        self.intensitySlider.valueChanged.connect(self._changeBlurIntensity)
        self.intensitySlider.setFixedHeight(Settings.Common.Sizes.SLIDER_HEIGHT)
        layout.addWidget(self.intensitySlider)

        # Angle control with preview
        angleLayout = QHBoxLayout()
        
        # Angle preview
        self.anglePreview = QLabel()
        self.anglePreview.setFixedSize(Settings.Text.SPINBOX_SIZE, Settings.Text.SPINBOX_SIZE)
        self._updateAnglePreview()
        
        # Angle controls container
        angleContainer = QWidget()
        angleContainer.setFixedSize(*Settings.Text.ANGLE_CONTAINER_SIZE)
        
        angleControlLayout = QVBoxLayout(angleContainer)
        angleControlLayout.setContentsMargins(0, 0, 0, 0)
        
        angleSliderLayout = QHBoxLayout()
        angleSliderLayout.setSpacing(5)
        
        # Angle slider
        self.angleSlider = QSlider(Qt.Horizontal)
        self.angleSlider.setMinimum(Settings.Blur.ANGLE['MIN'])
        self.angleSlider.setMaximum(Settings.Blur.ANGLE['MAX'])
        self.angleSlider.setValue(self.blur_angle)
        self.angleSlider.setTickPosition(QSlider.TicksBelow)
        self.angleSlider.setTickInterval(Settings.Text.ANGLE_TICK_INTERVAL)
        
        # Angle spinbox
        self.angleSpinBox = QSpinBox(self)
        self.angleSpinBox.setMinimum(Settings.Blur.ANGLE['MIN'])
        self.angleSpinBox.setMaximum(Settings.Blur.ANGLE['MAX'])
        self.angleSpinBox.setValue(self.blur_angle)
        self.angleSpinBox.setFixedWidth(Settings.Text.SPINBOX_SIZE)
        self.angleSpinBox.setSuffix("°")
        
        # Connect angle control signals
        self.angleSlider.valueChanged.connect(self._changeBlurAngle)
        self.angleSpinBox.valueChanged.connect(self._changeBlurAngle)
        
        # Add controls to layouts
        angleSliderLayout.addWidget(self.angleSlider)
        angleSliderLayout.addWidget(self.angleSpinBox)
        angleControlLayout.addLayout(angleSliderLayout)
        angleLayout.addWidget(self.anglePreview)
        angleLayout.addWidget(angleContainer)
        
        layout.addLayout(angleLayout)

        # Apply blur button
        self.applyBlurButton = QPushButton(
            Settings.get_button_text_with_shortcut(Settings.ButtonText.Tools.APPLY_BLUR),
            self
        )
        self.applyBlurButton.clicked.connect(self.applyBlur)
        self.applyBlurButton.setFixedHeight(Settings.Common.Sizes.BUTTON_HEIGHT)
        layout.addWidget(self.applyBlurButton)

        self.setLayout(layout)

    def _updateAnglePreview(self):
        """Update angle preview with a motion blur line"""
        preview = QPixmap(Settings.Text.SPINBOX_SIZE, Settings.Text.SPINBOX_SIZE)
        preview.fill(Qt.white)
        
        painter = QPainter(preview)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw border
        painter.setPen(Qt.lightGray)
        painter.drawRect(0, 0, Settings.Text.SPINBOX_SIZE-1, Settings.Text.SPINBOX_SIZE-1)
        
        # Move to center and rotate
        painter.translate(Settings.Text.SPINBOX_SIZE/2, Settings.Text.SPINBOX_SIZE/2)
        painter.rotate(self.blur_angle)
        
        # Draw motion blur line
        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        line_length = int(Settings.Text.SPINBOX_SIZE * 0.7)
        painter.drawLine(int(-line_length/2), 0, int(line_length/2), 0)
        
        # Draw arrow heads
        arrow_size = 4
        painter.drawLine(
            int(line_length/2), 0, 
            int(line_length/2 - arrow_size), -arrow_size
        )
        painter.drawLine(
            int(line_length/2), 0, 
            int(line_length/2 - arrow_size), arrow_size
        )
        painter.drawLine(
            int(-line_length/2), 0, 
            int(-line_length/2 + arrow_size), -arrow_size
        )
        painter.drawLine(
            int(-line_length/2), 0, 
            int(-line_length/2 + arrow_size), arrow_size
        )
        
        painter.end()
        self.anglePreview.setPixmap(preview)

    def _changeBlurIntensity(self, value):
        """Update blur intensity based on slider value"""
        self.blur_intensity = value
        self.intensityLabel.setText(Settings.Blur.INTENSITY_LABEL_TEXT.format(self.blur_intensity))

    def _changeBlurAngle(self, value):
        """Update blur angle based on slider value"""
        self.blur_angle = value
        # Sync the other control
        if self.sender() == self.angleSlider:
            self.angleSpinBox.setValue(value)
        else:
            self.angleSlider.setValue(value)
        self._updateAnglePreview()

    def applyBlur(self):
        """Apply motion blur effect to the selected area"""
        pixmap = self.image_and_selection_source.getImage()
        selection_polygon = self.image_and_selection_source.getSelectionPolygon()

        if pixmap and len(selection_polygon) > 0:
            # Convert QPixmap to PIL Image
            pil_image = pixmap_to_pil_image_with_alpha(pixmap)
            
            # Apply motion blur effect
            result_image = apply_optimized_motion_blur_to_polygon(
                pil_image, 
                selection_polygon, 
                self.blur_intensity,
                self.blur_angle
            )
            
            # Convert back to QPixmap and update image
            result_pixmap = QPixmap.fromImage(pil_image_to_qimage_with_alpha(result_image))
            self.image_and_selection_source.setImage(result_pixmap) 