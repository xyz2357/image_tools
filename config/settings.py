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


class MosaicWidgetSettings:
    """Settings for mosaic tool"""
    MOSAIC_SIZE = {
        'MIN': 1,
        'MAX': 10,
        'DEFAULT': 20
    }
    SIZE_MULTIPLIER = 5
    SIZE_LABEL_TEXT = "Mosaic Size: {}"
    BUTTON_TEXT = "Apply Mosaic"


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
    BUTTON_TEXT = "Add Text"


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

    class Buttons:
        OPEN = "Open Image"
        SAVE = "Save Image"
        UNDO = "Undo"
        REDO = "Redo"
        TOGGLE_MODE = "Toggle Selection Mode - Current: {}"


class ShortcutSettings:
    """Keyboard shortcuts"""
    class File:
        OPEN = "Ctrl+O"
        SAVE = "Ctrl+S"
    
    class Edit:
        UNDO = "Ctrl+Z"
        REDO = "Ctrl+Shift+Z"
    
    class Tools:
        TOGGLE_SELECT = "Tab"
        APPLY_TEXT = "Ctrl+T"
        APPLY_MOSAIC = "Ctrl+M"


class Settings:
    """Settings manager that provides access to all settings"""
    Common = CommonWidgetSettings
    Text = TextWidgetSettings
    Mosaic = MosaicWidgetSettings
    Image = ImageSelectionWidgetSettings
    Shortcut = ShortcutSettings 