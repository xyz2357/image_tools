import unittest
from unittest.mock import patch
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.append(str(Path(__file__).parent.parent.parent))

from ui.main_window import runMainWindow, MainWindow


class TestButtonStability(unittest.TestCase):
    """Test all buttons to ensure they don't crash the application"""
    
    @classmethod
    def setUpClass(cls):
        """Create the application once for all tests"""
        cls.app = QApplication([])

    def setUp(self):
        """Create a fresh window for each test"""
        self.window = MainWindow()

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName')
    @patch('PyQt5.QtWidgets.QFileDialog.getSaveFileName')
    @patch('PyQt5.QtWidgets.QColorDialog.getColor')
    def test_all_buttons(self, mock_color_dialog, mock_save_dialog, mock_open_dialog):
        """Test clicking all buttons in the application"""
        # 模拟对话框返回值
        mock_open_dialog.return_value = ('', '')  # (文件路径, 文件类型)
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