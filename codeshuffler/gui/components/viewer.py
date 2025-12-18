from PyQt5.QtWidgets import QSizePolicy, QTextBrowser, QVBoxLayout, QWidget


class HtmlPreviewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )

        self._web = None
        self._text = None

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        container = QWidget(self)
        container.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        text = QTextBrowser(container)
        text.setOpenExternalLinks(True)
        text.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )

        self._text = text
        container_layout.addWidget(text)

        root_layout.addWidget(container)
        self.setLayout(root_layout)

    def set_message(self, msg: str):
        html = f"""
        <html>
          <body style="
            background:#ffffff;
            color:#666666;
            font-family:Segoe UI, Arial;
          ">
            <div style="padding:16px;">
              {msg}
            </div>
          </body>
        </html>
        """
        self.set_html(html)

    def set_html(self, html: str):
        if self._web is not None:
            self._web.setHtml(html)
        elif self._text is not None:
            self._text.setHtml(html)
