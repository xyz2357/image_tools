import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication
import sys
import os

class TestButtonStability(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 设置平台为 offscreen
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
        
        # 检查是否已经有 QApplication 实例
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)
        else:
            cls.app = QApplication.instance()

    def setUp(self):
        from ui.main_window import MainWindow
        self.window = MainWindow()
        # 不需要实际显示窗口
        # self.window.show()

    def tearDown(self):
        self.window.close()
        QTest.qWait(100)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'app'):
            cls.app.quit()

    def test_all_buttons(self):
        # 修改测试代码，不依赖实际的显示
        # ... 