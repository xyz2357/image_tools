from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence


def create_shortcut(parent, key_sequence: str, slot):
    """Create and connect a shortcut
    
    Args:
        parent: Parent widget for the shortcut
        key_sequence: Keyboard sequence (e.g. "Ctrl+S")
        slot: Function to connect to the shortcut
    
    Returns:
        QShortcut: The created shortcut
    """
    shortcut = QShortcut(QKeySequence(key_sequence), parent)
    shortcut.activated.connect(slot)
    return shortcut