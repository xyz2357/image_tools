from PyQt5.QtWidgets import QFontComboBox
from PyQt5.QtGui import QFontDatabase

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