TITLE = """
QLabel {
    color: #000000;
    font-weight: bold;
    font-family: 'Segoe UI', 'Tahoma', sans-serif;
    padding: 5px 10px;
}
"""
MENU_BAR_STYLE = """
        QMenuBar {
            background-color: #252526;
            color: white;
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
    padding: 0px;
}
"""

DARK_TEXTEDIT_HIGHLIGHT = """
QPlainTextEdit, QTextEdit {
    background-color: #1e1e1e;
    color: #dcdcdc;
    font-family: 'Source Code Pro', 'Consolas', monospace;
}
"""

DARK_TEXTEDIT_ACTIVE = """
QPlainTextEdit, QTextEdit {
    background-color: #1e1e1e;
    color: #dcdcdc;
    font-family: 'Source Code Pro', 'Consolas', monospace;
}
"""
LIGHT_TEXTEDIT = """
QTextEdit {
    border: none;
    background-color: #ffffff;
    color: #000000;
    font-family: 'Segoe UI', 'Tahoma', sans-serif;
}
"""
ANSWER_LIST_STYLE = """
        QTreeWidget {
            border: none;
            background-color: #ffffff;
            font-family: 'Segoe UI', 'Tahoma', sans-serif;
        }

        QHeaderView::section {
            border-bottom: 1px solid #bdbdbd;
            font-weight: 600;
        }
        """

DARK_DROP_AREA = """
QPlainTextEdit {
    background-color: #1e1e1e;
    color: #dcdcdc;
    padding: 10px;
    font-family: 'Source Code Pro';
}
"""
LIGHT_DROP_AREA = """
QPlainTextEdit {
    background-color: #ffffff;
    color: #000000;
    padding: 10px;
    font-family: 'Source Code Pro', 'Consolas', monospace;
}
"""
LIGHT_DROP_AREA_HIGHLIGHT = """
QPlainTextEdit {
    background-color: #f5faff;   /* subtle blue tint */
    color: #000000;
    padding: 10px;
    font-family: 'Source Code Pro', 'Consolas', monospace;
}
"""
LIGHT_DROP_AREA_ACTIVE = """
QPlainTextEdit {
    background-color: #ffffff;
    color: #000000;
    padding: 10px;
    font-family: 'Source Code Pro', 'Consolas', monospace;
}
"""


TAB_STYLE = """
            QTabBar::tab {
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
                QWidget#SectionBody {
                    background-color: #ffffff;
                    border: 1px solid #bdbdbd;
                }
            """
