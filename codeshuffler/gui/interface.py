import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import (
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

from codeshuffler.lib import settings
from codeshuffler.lib.generator import (
    gen_correct_answer,
    gen_random_choices_wICinst,
    generate_partials,
    incorrect_instructions,
    read_original_code,
)
from codeshuffler.lib.utils import download_image, shuffle_sol

BASE_PATH = os.path.join(os.getcwd(), "codeshuffler", "gui", "codefiles")
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
        self.filename = None
        self.shuffled_question = None

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                self.save_dropped_file(file_path)

    def save_dropped_file(self, file_path):
        # to-do: implement an LRU cache to avoid overclutting folder
        filename = os.path.basename(file_path)
        self.filename = filename
        save_path = os.path.join(BASE_PATH, filename)
        print(f"Saving dropped file to: {save_path}")
        with open(file_path, "rb") as source:
            with open(save_path, "wb") as dest:
                dest.write(source.read())
        self.current_file = save_path
        self.drop_label.setText(f"File uploaded: {filename}")

    def browse_file(self, event):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select code file", "", "All Files (*.*)")
        if file_path:
            self.save_dropped_file(file_path)

    def shuffle_code(self):
        if not self.current_file:
            QMessageBox.warning(self, "No File", "Please upload a file first.")
            return
        read_code = open(self.current_file)
        correct_sol, wrong_inst, wrong_inst_dict = read_original_code(read_code)
        correct_sol_w_incorrect = incorrect_instructions(correct_sol, wrong_inst)

        # display shuffled question
        shuffled_code = shuffle_sol(correct_sol_w_incorrect)
        self.shuffled_question = shuffled_code
        formatted_code = "\n".join(shuffled_code)
        self.code_preview.setPlainText(formatted_code)

        correct_answer, remain_lines = gen_correct_answer(correct_sol, shuffled_code)
        partial_option = generate_partials(
            len(wrong_inst_dict), shuffled_code, wrong_inst_dict, correct_answer
        )
        random_choices = gen_random_choices_wICinst(
            correct_answer, settings.no_of_choices, remain_lines
        )
        self.answer_choices.clear()
        letters = ["a", "b", "c", "d", "e", "f", "g"]

        for i, choice in enumerate(random_choices):
            label = f"{letters[i]}) {choice}"
            self.answer_choices.addItem(label)
        if partial_option:
            self.answer_choices.addItem("")
            self.answer_choices.addItem("**Partial Credit Options**:")
            for i, p in enumerate(partial_option, start=1):
                self.answer_choices.addItem(f"{i}) {p}")

    def download_png(self):
        if not self.code_preview.toPlainText():
            QMessageBox.warning(self, "No Code", "No shuffled code to download.")
            return

        image_shuffled_sol = []

        for el in range(len(self.shuffled_question)):
            line = self.shuffled_question[el].split(")", 1)
            image_shuffled_sol.append(line[0] + ") " + line[-1].strip())

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save as PNG", "shuffled_code.png", "PNG Files (*.png)"
        )
        if file_path:
            try:
                download_image(image_shuffled_sol, file_path)
                QMessageBox.information(self, "Saved", f"Shuffled code saved to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save PNG: {e}")

    def open_settings(self):
        QMessageBox.information(self, "Settings", "Settings window coming soon.")
