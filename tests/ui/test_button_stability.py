import os
import sys
import unittest
from unittest.mock import patch
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

# 获取项目根目录
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

# 添加项目根目录到 Python 路径
sys.path.insert(0, project_root)

# 导入
from ui.main_window import MainWindow


class TestButtonStability(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 检查是否已经有 QApplication 实例
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)
        else:
            cls.app = QApplication.instance()
        
        # 确保应用程序正确初始化
        if not cls.app.thread():
            cls.app.moveToThread(QApplication.instance().thread())

    def setUp(self):
        self.window = MainWindow()
        self.window.show()

    def tearDown(self):
        self.window.close()
        QTest.qWait(100)  # 等待窗口完全关闭

    @classmethod
    def tearDownClass(cls):
        # 清理应用程序
        if hasattr(cls, 'app'):
            cls.app.quit()

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName')
    @patch('PyQt5.QtWidgets.QFileDialog.getSaveFileName')
    @patch('PyQt5.QtWidgets.QColorDialog.getColor')
    def test_all_buttons(self, mock_color_dialog, mock_save_dialog, mock_open_dialog):
        mock_open_dialog.return_value = ('', '')
        mock_save_dialog.return_value = ('', '')
        mock_color_dialog.return_value = QColor(Qt.red)

        # 收集所有按钮
        buttons_to_test = [
            # ImageAndSelectionWidget buttons
            (self.window.imageAndSelectionWidget.openImageButton, "Open Image"),
            (self.window.imageAndSelectionWidget.saveButton, "Save Image"),
            (self.window.imageAndSelectionWidget.undoButton, "Undo"),
            (self.window.imageAndSelectionWidget.redoButton, "Redo"),
            (self.window.imageAndSelectionWidget.toggleSelectionModeButton, "Toggle Selection"),
            
            # TextWidget buttons
            (self.window.textWidget.applyTextButton, "Apply Text"),
            (self.window.textWidget.colorButton, "Color Button"),
            
            # MosaicWidget buttons
            (self.window.mosaicWidget.applyMosaicButton, "Apply Mosaic"),
        ]

        # 测试每个按钮
        for button, button_name in buttons_to_test:
            with self.subTest(button=button_name):
                try:
                    QTest.mouseClick(button, Qt.LeftButton)
                except Exception as e:
                    self.fail(f"Button '{button_name}' crashed with error: {str(e)}")

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName')
    @patch('PyQt5.QtWidgets.QFileDialog.getSaveFileName')
    def test_all_shortcuts(self, mock_save_dialog, mock_open_dialog):
        """Test all shortcuts in the application"""
        # 模拟对话框返回值
        mock_open_dialog.return_value = ('', '')
        mock_save_dialog.return_value = ('', '')

        shortcuts_to_test = [
            # File operations
            ((Qt.ControlModifier, Qt.Key_O), "Ctrl+O (Open)"),
            ((Qt.ControlModifier, Qt.Key_S), "Ctrl+S (Save)"),
            
            # Edit operations
            ((Qt.ControlModifier, Qt.Key_Z), "Ctrl+Z (Undo)"),
            ((Qt.ControlModifier | Qt.ShiftModifier, Qt.Key_Z), "Ctrl+Shift+Z (Redo)"),
            
            # Tool operations
            ((Qt.NoModifier, Qt.Key_Tab), "Tab (Toggle Selection)"),
            ((Qt.ControlModifier, Qt.Key_T), "Ctrl+T (Apply Text)"),
            ((Qt.ControlModifier, Qt.Key_M), "Ctrl+M (Apply Mosaic)"),
        ]

        # 测试每个快捷键
        for (modifier, key), shortcut_name in shortcuts_to_test:
            with self.subTest(shortcut=shortcut_name):
                try:
                    QTest.keyClick(self.window, key, modifier)
                except Exception as e:
                    self.fail(f"Shortcut '{shortcut_name}' crashed with error: {str(e)}")

    def test_slider_interactions(self):
        """Test all sliders in the application"""
        sliders_to_test = [
            # TextWidget sliders
            (self.window.textWidget.sizeSlider, "Text Size"),
            (self.window.textWidget.angleSlider, "Text Angle"),
            
            # MosaicWidget slider
            (self.window.mosaicWidget.sizeSlider, "Mosaic Size"),
        ]

        # 测试每个滑块的极值和中间值
        for slider, slider_name in sliders_to_test:
            with self.subTest(slider=slider_name):
                try:
                    # 测试最小值
                    slider.setValue(slider.minimum())
                    # 测试中间值
                    slider.setValue((slider.minimum() + slider.maximum()) // 2)
                    # 测试最大值
                    slider.setValue(slider.maximum())
                except Exception as e:
                    self.fail(f"Slider '{slider_name}' crashed with error: {str(e)}")


if __name__ == '__main__':
    unittest.main() 