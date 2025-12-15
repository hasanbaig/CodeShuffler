TITLE = """
QLabel {
    color: #000000;
    font-size: 18px;
    font-weight: bold;
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    padding: 5px 10px;
}
"""
MENU_BAR_STYLE = """
        QMenuBar {
            background-color: #252526;
            color: white;
            font-size: 13px;
            padding: 4px;
        }
        QMenuBar::item:selected {
            background-color: #3a3a3a;
        }
        QMenu {
            background-color: #2d2d2d;
            color: white;
            border: 1px solid #3c3c3c;
        }
        QMenu::item:selected {
            background-color: #3c3c3c;
        }
    """
DARK_TEXTEDIT_BASE = """
QPlainTextEdit, QTextEdit {
    border: 2px solid #aaa;
    border-radius: 8px;
    background-color: #1e1e1e;
    color: #dcdcdc;
    font-family: 'Source Code Pro', 'Consolas', monospace;
    font-size: 13px;
    padding: 10px;
}
"""

DARK_TEXTEDIT_HIGHLIGHT = """
QPlainTextEdit, QTextEdit {
    border: 2px solid #00bfff;
    border-radius: 8px;
    background-color: #1e1e1e;
    color: #dcdcdc;
    font-family: 'Source Code Pro', 'Consolas', monospace;
    font-size: 13px;
    padding: 10px;
}
"""

DARK_TEXTEDIT_ACTIVE = """
QPlainTextEdit, QTextEdit {
    border: 2px solid #555;
    border-radius: 8px;
    background-color: #1e1e1e;
    color: #dcdcdc;
    font-family: 'Source Code Pro', 'Consolas', monospace;
    font-size: 13px;
    padding: 10px;
}
"""

DARK_DROP_AREA = """
QPlainTextEdit {
    border: 2px dashed #888;
    border-radius: 8px;
    background-color: #1e1e1e;
    color: #dcdcdc;
    padding: 10px;
    font-family: 'Source Code Pro';
}
"""
