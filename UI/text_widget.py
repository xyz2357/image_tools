from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QWidget, QPushButton, 
                           QSlider, QLineEdit, QColorDialog, QHBoxLayout,
                           QSpinBox, QFontComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QFont, QFontDatabase, QColor
from config.fonts import FONT_LIST
from config.text_widget_settings import *  # Import all settings


class CustomFontComboBox(QFontComboBox):
    def __init__(self, allowed_fonts, parent=None):
        super().__init__(parent)
        self.allowed_fonts = allowed_fonts
        self._filterFonts()
    
    def _filterFonts(self):
        # Remove all current items
        self.clear()
        
        # Get all available fonts
        font_db = QFontDatabase()
        available_fonts = set(font_db.families())
        
        # Keep only allowed fonts
        filtered_fonts = self.allowed_fonts.intersection(available_fonts)
        
        # Temporarily block signals to avoid multiple updates
        self.blockSignals(True)
        
        # Add items for each filtered font
        for font in sorted(filtered_fonts):
            self.addItem(font)
            
        self.blockSignals(False) 


class TextWidget(QWidget):
    ALLOWED_FONTS = FONT_LIST

    def __init__(self, image_and_selection_source):
        super().__init__()
        self.textSize = TEXT_SIZE_DEFAULT
        self.textColor = QColor(*DEFAULT_TEXT_COLOR)
        self.currentFont = QFont()
        self.textAngle = TEXT_ANGLE_DEFAULT
        self.image_and_selection_source = image_and_selection_source
        self._initUI()

    def _initUI(self):
        layout = QVBoxLayout()

        # Text input box
        self.textInput = QLineEdit(self)
        self.textInput.setPlaceholderText(PLACEHOLDER_TEXT)
        layout.addWidget(self.textInput)

        # Font selection
        fontLayout = QHBoxLayout()
        self.fontComboBox = CustomFontComboBox(self.ALLOWED_FONTS, self)
        self.fontComboBox.currentFontChanged.connect(self._changeFont)
        if self.fontComboBox.count() > 0:
            self.currentFont = self.fontComboBox.currentFont()
        fontLayout.addWidget(QLabel(FONT_LABEL))
        fontLayout.addWidget(self.fontComboBox)
        layout.addLayout(fontLayout)

        # Color selection
        colorLayout = QHBoxLayout()
        self.colorButton = QPushButton(COLOR_BUTTON_TEXT, self)
        self.colorButton.clicked.connect(self._chooseColor)
        self.colorPreview = QLabel()
        self.colorPreview.setFixedSize(COLOR_PREVIEW_SIZE, COLOR_PREVIEW_SIZE)
        self._updateColorPreview()
        colorLayout.addWidget(self.colorButton)
        colorLayout.addWidget(self.colorPreview)
        layout.addLayout(colorLayout)

        # Text size control
        sizeLayout = QHBoxLayout()
        self.sizeLabel = QLabel(TEXT_SIZE_LABEL, self)
        self.sizeSlider = QSlider(Qt.Horizontal, self)
        self.sizeSlider.setMinimum(TEXT_SIZE_MIN)
        self.sizeSlider.setMaximum(TEXT_SIZE_MAX)
        self.sizeSlider.setValue(self.textSize)
        
        self.sizeSpinBox = QSpinBox(self)
        self.sizeSpinBox.setMinimum(TEXT_SIZE_MIN)
        self.sizeSpinBox.setMaximum(TEXT_SIZE_MAX)
        self.sizeSpinBox.setValue(self.textSize)
        self.sizeSpinBox.setFixedWidth(SPINBOX_WIDTH)
        
        self.sizeSlider.valueChanged.connect(self._changeTextSize)
        self.sizeSpinBox.valueChanged.connect(self._changeTextSize)
        
        sizeLayout.addWidget(self.sizeLabel)
        sizeLayout.addWidget(self.sizeSlider)
        sizeLayout.addWidget(self.sizeSpinBox)
        layout.addLayout(sizeLayout)

        # Angle control
        angleLayout = QHBoxLayout()
        self.anglePreview = QLabel()
        self.anglePreview.setFixedSize(PREVIEW_SIZE, PREVIEW_SIZE)
        self._updateAnglePreview()
        
        angleContainer = QWidget()
        angleContainer.setFixedSize(*ANGLE_CONTAINER_SIZE)
        
        angleControlLayout = QVBoxLayout(angleContainer)
        angleControlLayout.setContentsMargins(0, 0, 0, 0)
        
        angleSliderLayout = QHBoxLayout()
        angleSliderLayout.setSpacing(5)
        
        self.angleLabel = QLabel(TEXT_ANGLE_LABEL, self)
        self.angleSlider = QSlider(Qt.Horizontal)
        self.angleSlider.setMinimum(TEXT_ANGLE_MIN)
        self.angleSlider.setMaximum(TEXT_ANGLE_MAX)
        self.angleSlider.setValue(TEXT_ANGLE_DEFAULT)
        self.angleSlider.setTickPosition(QSlider.TicksBelow)
        self.angleSlider.setTickInterval(TEXT_ANGLE_TICK_INTERVAL)
        
        self.angleSpinBox = QSpinBox(self)
        self.angleSpinBox.setMinimum(TEXT_ANGLE_MIN)
        self.angleSpinBox.setMaximum(TEXT_ANGLE_MAX)
        self.angleSpinBox.setValue(TEXT_ANGLE_DEFAULT)
        self.angleSpinBox.setFixedWidth(SPINBOX_WIDTH)
        self.angleSpinBox.setSuffix("°")
        
        # Connect signals
        self.angleSlider.valueChanged.connect(self._changeAngle)
        self.angleSpinBox.valueChanged.connect(self._changeAngle)
        
        angleSliderLayout.addWidget(self.angleLabel)
        angleSliderLayout.addWidget(self.angleSlider)
        angleSliderLayout.addWidget(self.angleSpinBox)
        
        angleControlLayout.addLayout(angleSliderLayout)
        
        angleLayout.addWidget(self.anglePreview)
        angleLayout.addWidget(angleContainer)
        layout.addLayout(angleLayout)

        # Apply text button
        self.applyTextButton = QPushButton(ADD_TEXT_BUTTON, self)
        self.applyTextButton.clicked.connect(self.applyText)
        layout.addWidget(self.applyTextButton)
        self.applyTextButton.setFixedHeight(BUTTON_HEIGHT)

        self.setLayout(layout)
        self.setMaximumHeight(300)

    def _updateColorPreview(self):
        preview = QPixmap(COLOR_PREVIEW_SIZE, COLOR_PREVIEW_SIZE)
        preview.fill(self.textColor)
        self.colorPreview.setPixmap(preview)

    def _chooseColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.textColor = color
            self._updateColorPreview()

    def _changeFont(self, font):
        self.currentFont = font

    def _changeTextSize(self, value):
        """Update text size"""
        self.textSize = value
        # Sync the other control
        if self.sender() == self.sizeSlider:
            self.sizeSpinBox.setValue(value)
        else:
            self.sizeSlider.setValue(value)

    def _updateAnglePreview(self):
        """Update angle preview"""
        preview = QPixmap(PREVIEW_SIZE, PREVIEW_SIZE)
        preview.fill(Qt.white)
        
        painter = QPainter(preview)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw border
        painter.setPen(Qt.lightGray)
        painter.drawRect(0, 0, PREVIEW_SIZE-1, PREVIEW_SIZE-1)
        
        # Draw text
        painter.setPen(self.textColor)
        font = QFont(self.currentFont)
        font.setPointSize(PREVIEW_FONT_SIZE)  # Smaller font size for preview
        painter.setFont(font)
        
        # Move to center point and rotate
        painter.translate(PREVIEW_SIZE/2, PREVIEW_SIZE/2)
        painter.rotate(self.textAngle)
        
        # Draw sample text
        text = PREVIEW_SAMPLE_TEXT
        text_width = painter.fontMetrics().horizontalAdvance(text)
        text_height = painter.fontMetrics().height()
        painter.drawText(int(-text_width/2), int(text_height/4), text)
        
        painter.end()
        self.anglePreview.setPixmap(preview)

    def _changeAngle(self, value):
        """Update text angle"""
        self.textAngle = value
        # Sync the other control
        if self.sender() == self.angleSlider:
            self.angleSpinBox.setValue(value)
        else:
            self.angleSlider.setValue(value)
        self._updateAnglePreview()

    def applyText(self):
        pixmap = self.image_and_selection_source.getImage()
        selection_points = self.image_and_selection_source.getSelectionPolygon()
        text = self.textInput.text()

        if pixmap and len(selection_points) > 0 and text:
            new_pixmap = QPixmap(pixmap)
            painter = QPainter(new_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            font = QFont(self.currentFont)
            font.setPointSize(self.textSize)
            painter.setFont(font)
            painter.setPen(self.textColor)

            # Calculate selection center point
            x_coords = [p[0] for p in selection_points]
            y_coords = [p[1] for p in selection_points]
            center_x = (min(x_coords) + max(x_coords)) / 2
            center_y = (min(y_coords) + max(y_coords)) / 2

            # Save current painter state
            painter.save()
            
            # Move to center point and rotate
            painter.translate(center_x, center_y)
            painter.rotate(self.textAngle)
            
            # Calculate text dimensions
            metrics = painter.fontMetrics()
            text_width = metrics.horizontalAdvance(text)
            text_height = metrics.height()
            
            # Draw text (offset from center point)
            painter.drawText(int(-text_width/2), int(text_height/4), text)
            
            # Restore painter state
            painter.restore()
            painter.end()

            self.image_and_selection_source.setImage(new_pixmap) 