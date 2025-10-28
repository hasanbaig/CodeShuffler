import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

# Assuming these functions exist in the existing CodeShuffler project
# from codeshuffler.core import shuffle_code, generate_multiple_choice, save_code_as_png

BASE_PATH = os.path.join(os.getcwd(), "CodeShuffler", "codeshuffler", "codefiles")
os.makedirs(BASE_PATH, exist_ok=True)


class CodeShufflerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeShuffler")
        self.setAcceptDrops(True)
        self.setGeometry(200, 100, 900, 600)

        # Layouts
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # --- Left Side (Drop Zone + Buttons) ---
        self.drop_label = QLabel(
            "Drop code file here or click to browse\n(JS, TS, Python, Java, C++, etc.)"
        )
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.drop_label.setStyleSheet("border: 2px dashed #ccc; font-size: 14px; padding: 60px;")
        self.drop_label.mousePressEvent = self.browse_file

        self.shuffle_btn = QPushButton("Shuffle")
        self.shuffle_btn.clicked.connect(self.shuffle_code)

        self.settings_btn = QPushButton("Settings")
        self.settings_btn.clicked.connect(self.open_settings)

        left_layout.addWidget(self.drop_label)
        left_layout.addWidget(self.shuffle_btn)
        left_layout.addWidget(self.settings_btn)

        # --- Right Side (Code Preview + Multiple Choice) ---
        self.code_preview = QTextEdit()
        self.code_preview.setReadOnly(True)
        self.code_preview.setPlaceholderText("Shuffled code will appear here...")

        self.answer_choices = QListWidget()
        self.answer_choices.addItem("Multiple choice options will appear here...")

        self.download_btn = QPushButton("Download PNG")
        self.download_btn.clicked.connect(self.download_png)

        right_layout.addWidget(QLabel("Shuffled Code"))
        right_layout.addWidget(self.code_preview)
        right_layout.addWidget(QLabel("Answer Choices"))
        right_layout.addWidget(self.answer_choices)
        right_layout.addWidget(self.download_btn)

        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 3)

        self.setLayout(main_layout)
        self.current_file = None

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                self.save_dropped_file(file_path)

    def save_dropped_file(self, file_path):
        try:
            filename = os.path.basename(file_path)
            save_path = os.path.join(BASE_PATH, filename)
            with open(file_path, "rb") as src, open(save_path, "wb") as dst:
                dst.write(src.read())
            self.current_file = save_path
            self.drop_label.setText(f"File uploaded: {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {e}")

    def browse_file(self, event):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select code file", "", "All Files (*.*)")
        if file_path:
            self.save_dropped_file(file_path)

    def shuffle_code(self):
        if not self.current_file:
            QMessageBox.warning(self, "No File", "Please upload a file first.")
            return

        # Replace with real shuffle logic
        shuffled_code = f"# Shuffled version of {os.path.basename(self.current_file)}\nprint('Hello from shuffled code!')"
        self.code_preview.setPlainText(shuffled_code)

        # Replace with real multiple choice logic
        self.answer_choices.clear()
        self.answer_choices.addItems(
            [
                "Option A: Correct order",
                "Option B: Random order",
                "Option C: Missing function",
                "Option D: Extra line",
            ]
        )

    def download_png(self):
        if not self.code_preview.toPlainText():
            QMessageBox.warning(self, "No Code", "No shuffled code to download.")
            return

        # Replace with real save logic
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save as PNG", "shuffled_code.png", "PNG Files (*.png)"
        )
        if file_path:
            try:
                # save_code_as_png(self.code_preview.toPlainText(), file_path)
                QMessageBox.information(self, "Saved", f"Shuffled code saved to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save PNG: {e}")

    def open_settings(self):
        QMessageBox.information(self, "Settings", "Settings window coming soon.")


if __name__ == "__main__":
    app = QApplication([])
    gui = CodeShufflerGUI()
    gui.show()
    app.exec_()
