class CommonWidgetSettings:
    """Common settings shared across all widgets"""
    class Sizes:
        MAIN_WINDOW_X = 200
        MAIN_WINDOW_Y = 200
        MAIN_WINDOW_WIDTH = 1024
        MAIN_WINDOW_HEIGHT = 768
        BUTTON_HEIGHT = 40
        SLIDER_HEIGHT = 30
        LABEL_HEIGHT = 20
        INPUT_HEIGHT = 30


class ShortcutSettings:
    """Centralized shortcut definitions"""
    # File operations 
    class File:
        OPEN = "Ctrl+O"
        SAVE = "Ctrl+S"
    
    # Edit operations
    class Edit:
        UNDO = "Ctrl+Z"
        REDO = "Ctrl+Shift+Z"
        TOGGLE_SELECT = "Tab"

    # Tool operations
    class Tools:
        APPLY_TEXT = None
        APPLY_MOSAIC = "Ctrl+M"
        APPLY_BLUR = "Ctrl+B"
        APPLY_CAMERA_EFFECT = None

class ButtonTextSettings:
    """Button text settings with optional shortcuts"""
    class File:
        OPEN = ("Open Image", ShortcutSettings.File.OPEN)
        SAVE = ("Save Image", ShortcutSettings.File.SAVE)
    
    class Edit:
        UNDO = ("Undo", ShortcutSettings.Edit.UNDO)
        REDO = ("Redo", ShortcutSettings.Edit.REDO)
        TOGGLE_MODE = ("Toggle Selection Mode - Current: {}", ShortcutSettings.Edit.TOGGLE_SELECT)
    
    class Tools:
        APPLY_TEXT = ("Add Text", ShortcutSettings.Tools.APPLY_TEXT)
        APPLY_MOSAIC = ("Apply Mosaic", ShortcutSettings.Tools.APPLY_MOSAIC)
        APPLY_BLUR = ("Apply Blur", ShortcutSettings.Tools.APPLY_BLUR)
        APPLY_CAMERA_EFFECT = ("Apply Camera Effect", ShortcutSettings.Tools.APPLY_CAMERA_EFFECT)


class TextWidgetSettings:
    """Settings for text tool"""
    PLACEHOLDER_TEXT = "Enter text here..."
    FONT_LIST = {
        "Arial",
        "Times New Roman",
        "Helvetica",
        "Courier New",
        "Microsoft YaHei",
        "SimSun",
    }
    FONT_LABEL = "Font:"
    COLOR_BUTTON_TEXT = "Choose Color"
    COLOR_PREVIEW_SIZE = 20
    DEFAULT_COLOR = (0, 0, 0)
    PREVIEW_SAMPLE_TEXT = "Aa"
    SPINBOX_SIZE = 50
    PREVIEW_FONT_SIZE = 12
    FONT_SIZE = {
        'MIN': 8,
        'MAX': 72,
        'DEFAULT': 20
    }
    ANGLE = {
        'MIN': -90,
        'MAX': 90,
        'DEFAULT': 0
    }
    ANGLE_TICK_INTERVAL = 10
    ANGLE_CONTAINER_SIZE = (300, 70)


class MosaicWidgetSettings:
    """Settings for mosaic tool"""
    MOSAIC_SIZE = {
        'MIN': 1,
        'MAX': 10,
        'DEFAULT': 20
    }
    SIZE_MULTIPLIER = 5
    SIZE_LABEL_TEXT = "Mosaic Size: {}"


class ImageSelectionWidgetSettings:
    """Settings for image and selection handling"""
    class Selection:
        PEN_COLOR = (255, 0, 0)  # Red
        PEN_WIDTH = 2
        MODES = {
            'RECT': "RECT",
            'LASSO': "LASSO"
        }

    class FileDialog:
        OPEN_TITLE = "Open Image"
        SAVE_TITLE = "Save Image"
        IMAGE_FILTER = "Images (*.png *.jpg *.jpeg)"
        SAVE_FILTER = "JPG Files (*.jpg *.jpeg);;PNG Files (*.png);;All Files (*)"


class Settings:
    """Settings manager that provides access to all settings"""
    Common = CommonWidgetSettings
    Text = TextWidgetSettings
    Mosaic = MosaicWidgetSettings
    Image = ImageSelectionWidgetSettings
    Shortcut = ShortcutSettings
    ButtonText = ButtonTextSettings

    class Blur:
        INTENSITY = {
            'MIN': 5,
            'MAX': 50,
            'DEFAULT': 20
        }
        ANGLE = {
            'MIN': 0,
            'MAX': 180,
            'DEFAULT': 90
        }
        INTENSITY_LABEL_TEXT = "Blur Intensity: {}"
        ANGLE_LABEL_TEXT = "Blur Angle: {}°"

    class Camera:
        # Battery level settings
        BATTERY_LEVEL = {
            'MIN': 0,
            'MAX': 100,
            'DEFAULT': 1.0
        }
        
        # Timer text settings
        TIMER_TEXT = {
            'DEFAULT': "00:00:00.000",
            'FORMAT': "HH:MM:SS.mmm"
        }
        
        # UI text
        BATTERY_LABEL_TEXT = "Battery: {:.0%}"
        TIMER_LABEL_TEXT = "Timer: HH:MM:SS.mmm"
        
    @staticmethod
    def get_button_text_with_shortcut(text_and_shortcut):
        text, shortcut = text_and_shortcut
        if shortcut:
            return f"{text} ({shortcut})"
        return text