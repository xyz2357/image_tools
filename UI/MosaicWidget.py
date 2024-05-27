import sys
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from utils.image_utils import pixmap_to_pil_image_with_alpha, pil_image_to_qimage_with_alpha, apply_mosaic

class MosaicWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.mosaicSize = 15  # 初始化马赛克大小
        self._initUI()

    def _initUI(self):
        layout = QVBoxLayout()

        # 马赛克效果应用按钮
        self.applyMosaicButton = QPushButton("Apply Mosaic", self)
        self.applyMosaicButton.clicked.connect(self.applyMosaic)
        layout.addWidget(self.applyMosaicButton)
        self.applyMosaicButton.setFixedHeight(100)

        # 创建 QLabel 来显示滑块的当前值
        self.sizeLabel = QLabel(f"Mosaic Size: {self.mosaicSize}", self)
        layout.addWidget(self.sizeLabel)

        # 创建滑块来调节马赛克大小
        self.sizeSlider = QSlider(Qt.Horizontal, self)
        self.sizeSlider.setMinimum(1)
        self.sizeSlider.setMaximum(8)
        self.sizeSlider.setValue(self.mosaicSize // 5)
        self.sizeSlider.valueChanged.connect(self._changeMosaicSize)
        layout.addWidget(self.sizeSlider)

        self.setLayout(layout)
        self.setMaximumHeight(200)

    def applyMosaic(self):
        pixmap = self.image_source.getImage()  #TODO: too ugly...
        selection_rect = self.image_source.getSelectionRect()

        if pixmap and not selection_rect.isNull():
            pil_image = pixmap_to_pil_image_with_alpha(pixmap)
            # 应用马赛克效果
            apply_mosaic(pil_image, (
                selection_rect.x(),
                selection_rect.y(),
                selection_rect.width(),
                selection_rect.height()
            ), self.mosaicSize)

            # 将 PIL Image 转换回 QImage
            result_pixmap = pil_image_to_qimage_with_alpha(pil_image)
            self.image_source.setImage(QPixmap.fromImage(result_pixmap))

    def _changeMosaicSize(self, value):
        self.mosaicSize = value * 5
        self.sizeLabel.setText(f"Mosaic Size: {self.mosaicSize}")  # 更新 QLabel 显示滑块的值

    def setImageSource(self, qImageWidget):
        self.image_source = qImageWidget

    # TODO: add button "auto" to set to 0.01 of long edge of the image and at least 4px
    # TODO: add different shape and doodling mosaic