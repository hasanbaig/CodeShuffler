from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

from codeshuffler.gui.utils.styles import BODY_STYLE, HEADER_STYLE


class Section(QWidget):
    def __init__(self, title: str, content: QWidget, *, dark_body=False, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QLabel(title)
        header.setStyleSheet(HEADER_STYLE)

        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(8, 6, 8, 6)
        body_layout.addWidget(content)

        if dark_body:
            body.setStyleSheet(
                """
                QWidget {
                    background-color: #1e1e1e;
                    border: 1px solid #bdbdbd;
                }
            """
            )
        else:
            body.setStyleSheet(BODY_STYLE)

        layout.addWidget(header)
        layout.addWidget(body)
