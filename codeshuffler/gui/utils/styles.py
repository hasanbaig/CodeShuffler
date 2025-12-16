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
    border: none;
    background-color: #1e1e1e;
    color: #dcdcdc;
    font-family: 'Source Code Pro', 'Consolas', monospace;
    font-size: 13px;
    padding: 0px;
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
}
"""
LIGHT_TEXTEDIT = """
QTextEdit {
    border: none;
    background-color: #ffffff;
    color: #000000;
    font-family: 'Segoe UI', 'Tahoma', sans-serif;
    font-size: 13px;
}
"""
ANSWER_LIST_STYLE = """
        QTreeWidget {
            border: none;
            background-color: #ffffff;
            font-family: Tahoma;
            font-size: 11px;
        }

        QHeaderView::section {
            border-bottom: 1px solid #bdbdbd;
            font-weight: 600;
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
TAB_STYLE = """
            QTabBar::tab {
                font-size: 10px;
            }
            QTabBar::tab:selected {
            }
        """
HEADER_STYLE = """
            QLabel {
                background-color: #f0f0f0;
                color: #000000;
                padding: 6px 10px;
                font-weight: 600;
                border: 1px solid #bdbdbd;
                border-bottom: none;
            }
        """
BODY_STYLE = """
                QWidget {
                    background-color: #ffffff;
                    border: 1px solid #bdbdbd;
                }
            """
