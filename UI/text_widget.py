from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QWidget, QPushButton, 
                           QSlider, QLineEdit, QColorDialog, QHBoxLayout,
                           QSpinBox, QFontComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor, QPainterPath, QFontDatabase
from config.fonts import FONT_LIST


class CustomFontComboBox(QFontComboBox):
    def __init__(self, allowed_fonts, parent=None):
        super().__init__(parent)
        self.allowed_fonts = allowed_fonts
        self._filterFonts()
    
    def _filterFonts(self):
        # 移除所有当前项
        self.clear()
        
        # 获取所有可用字体
        font_db = QFontDatabase()
        available_fonts = set(font_db.families())
        
        # 只保留允许的字体
        filtered_fonts = self.allowed_fonts.intersection(available_fonts)
        
        # 临时禁用信号以避免多次触发更新
        self.blockSignals(True)
        
        # 为每个过滤后的字体添加项
        for font in sorted(filtered_fonts):
            self.addItem(font)
            
        self.blockSignals(False) 


class TextWidget(QWidget):
    # 配置允许显示的字体列表
    ALLOWED_FONTS = FONT_LIST

    def __init__(self, image_and_selection_source):
        super().__init__()
        self.textSize = 20
        self.textColor = QColor(0, 0, 0)
        self.currentFont = QFont()
        self.textAngle = 0  # 默认角度为0
        self.image_and_selection_source = image_and_selection_source
        self._initUI()

    def _initUI(self):
        layout = QVBoxLayout()

        # 文本输入框
        self.textInput = QLineEdit(self)
        self.textInput.setPlaceholderText("Enter text here...")
        layout.addWidget(self.textInput)

        # 使用自定义字体选择框
        fontLayout = QHBoxLayout()
        self.fontComboBox = CustomFontComboBox(self.ALLOWED_FONTS, self)
        self.fontComboBox.currentFontChanged.connect(self._changeFont)
        
        # 如果有字体，设置第一个为默认字体
        if self.fontComboBox.count() > 0:
            self.currentFont = self.fontComboBox.currentFont()
            
        fontLayout.addWidget(QLabel("Font:"))
        fontLayout.addWidget(self.fontComboBox)
        layout.addLayout(fontLayout)

        # 颜色选择区域
        colorLayout = QHBoxLayout()
        self.colorButton = QPushButton("Choose Color", self)
        self.colorButton.clicked.connect(self._chooseColor)
        
        self.colorPreview = QLabel()
        self.colorPreview.setFixedSize(20, 20)
        self._updateColorPreview()
        
        colorLayout.addWidget(self.colorButton)
        colorLayout.addWidget(self.colorPreview)
        layout.addLayout(colorLayout)

        # 文字大小控制
        sizeLayout = QHBoxLayout()
        self.sizeLabel = QLabel("Text Size:", self)
        
        self.sizeSlider = QSlider(Qt.Horizontal, self)
        self.sizeSlider.setMinimum(8)
        self.sizeSlider.setMaximum(72)
        self.sizeSlider.setValue(self.textSize)
        
        self.sizeSpinBox = QSpinBox(self)
        self.sizeSpinBox.setMinimum(8)
        self.sizeSpinBox.setMaximum(72)
        self.sizeSpinBox.setValue(self.textSize)
        self.sizeSpinBox.setFixedWidth(50)  # 设置固定宽度
        
        # 连接信号
        self.sizeSlider.valueChanged.connect(self._changeTextSize)
        self.sizeSpinBox.valueChanged.connect(self._changeTextSize)
        
        sizeLayout.addWidget(self.sizeLabel)
        sizeLayout.addWidget(self.sizeSlider)
        sizeLayout.addWidget(self.sizeSpinBox)
        layout.addLayout(sizeLayout)

        # 角度控制
        angleLayout = QHBoxLayout()
        self.anglePreview = QLabel()
        self.anglePreview.setFixedSize(60, 60)
        self._updateAnglePreview()
        
        angleContainer = QWidget()
        angleContainer.setFixedSize(300, 70)
        
        angleControlLayout = QVBoxLayout(angleContainer)
        angleControlLayout.setContentsMargins(0, 0, 0, 0)
        
        # 角度控制的水平布局
        angleSliderLayout = QHBoxLayout()
        angleSliderLayout.setSpacing(5)
        
        self.angleLabel = QLabel("Text Angle:", self)
        self.angleSlider = QSlider(Qt.Horizontal)
        self.angleSlider.setMinimum(-90)
        self.angleSlider.setMaximum(90)
        self.angleSlider.setValue(0)
        self.angleSlider.setTickPosition(QSlider.TicksBelow)
        self.angleSlider.setTickInterval(15)
        
        self.angleSpinBox = QSpinBox(self)
        self.angleSpinBox.setMinimum(-90)
        self.angleSpinBox.setMaximum(90)
        self.angleSpinBox.setValue(0)
        self.angleSpinBox.setFixedWidth(50)
        self.angleSpinBox.setSuffix("°")
        
        # 连接信号
        self.angleSlider.valueChanged.connect(self._changeAngle)
        self.angleSpinBox.valueChanged.connect(self._changeAngle)
        
        angleSliderLayout.addWidget(self.angleLabel)
        angleSliderLayout.addWidget(self.angleSlider)
        angleSliderLayout.addWidget(self.angleSpinBox)
        
        angleControlLayout.addLayout(angleSliderLayout)
        
        angleLayout.addWidget(self.anglePreview)
        angleLayout.addWidget(angleContainer)
        layout.addLayout(angleLayout)

        # 应用文字按钮
        self.applyTextButton = QPushButton("Add Text", self)
        self.applyTextButton.clicked.connect(self.applyText)
        layout.addWidget(self.applyTextButton)
        self.applyTextButton.setFixedHeight(100)

        self.setLayout(layout)
        self.setMaximumHeight(300)

    def _updateColorPreview(self):
        preview = QPixmap(20, 20)
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
        """更新文字大小"""
        self.textSize = value
        # 同步更新另一个控件
        if self.sender() == self.sizeSlider:
            self.sizeSpinBox.setValue(value)
        else:
            self.sizeSlider.setValue(value)

    def _updateAnglePreview(self):
        """更新角度预览图"""
        preview = QPixmap(60, 60)
        preview.fill(Qt.white)
        
        painter = QPainter(preview)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制边框
        painter.setPen(Qt.lightGray)
        painter.drawRect(0, 0, 59, 59)
        
        # 绘制文字
        painter.setPen(self.textColor)
        font = QFont(self.currentFont)
        font.setPointSize(12)  # 预览用小一点的字号
        painter.setFont(font)
        
        # 移动到中心点并旋转
        painter.translate(30, 30)
        painter.rotate(self.textAngle)
        
        # 绘制示例文字
        text = "Aa"
        text_width = painter.fontMetrics().horizontalAdvance(text)
        text_height = painter.fontMetrics().height()
        painter.drawText(int(-text_width/2), int(text_height/4), text)
        
        painter.end()
        self.anglePreview.setPixmap(preview)

    def _changeAngle(self, value):
        """更新文字角度"""
        self.textAngle = value
        # 同步更新另一个控件
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

            # 计算选区中心点
            x_coords = [p[0] for p in selection_points]
            y_coords = [p[1] for p in selection_points]
            center_x = (min(x_coords) + max(x_coords)) / 2
            center_y = (min(y_coords) + max(y_coords)) / 2

            # 保存当前画笔状态
            painter.save()
            
            # 移动到中心点并旋转
            painter.translate(center_x, center_y)
            painter.rotate(self.textAngle)
            
            # 计算文本尺寸
            metrics = painter.fontMetrics()
            text_width = metrics.horizontalAdvance(text)
            text_height = metrics.height()
            
            # 绘制文本（从中心点偏移）
            painter.drawText(int(-text_width/2), int(text_height/4), text)
            
            # 恢复画笔状态
            painter.restore()
            painter.end()

            self.image_and_selection_source.setImage(new_pixmap) 