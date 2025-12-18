import os
import random

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QBrush, QColor, QIcon
from PyQt5.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from codeshuffler.gui.components.section import Section
from codeshuffler.gui.components.settings import SettingsDialog
from codeshuffler.gui.components.syntax import GenericHighlighter
from codeshuffler.gui.utils.dragdrop import FileDropHandler
from codeshuffler.gui.utils.styles import (
    ANSWER_LIST_STYLE,
    LIGHT_DROP_AREA,
    LIGHT_DROP_AREA_ACTIVE,
    LIGHT_DROP_AREA_HIGHLIGHT,
    LIGHT_TEXTEDIT,
)
from codeshuffler.lib.generator import (
    gen_correct_answer,
    gen_random_choices_wICinst,
    generate_partials,
    incorrect_instructions,
    shuffle_sol,
)
from codeshuffler.lib.utils import download_image, resource_path
from codeshuffler.models.codefile import CodeFile
from codeshuffler.models.languages import language_from_extension
from codeshuffler.settings import settings

BASE_PATH = os.path.join(os.getcwd(), "codeshuffler", "gui", "cache")
ICON_PATH = os.path.join("codeshuffler", "gui", "icons")
os.makedirs(BASE_PATH, exist_ok=True)


class CodeShufflerTab(QWidget, FileDropHandler):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file = None
        self.filename = None
        self.shuffled_question = None

        self.init_ui()
        self.init_events()
        self.enable_file_drop(self, self.handle_file_drop)

    def init_ui(self):
        layout = QVBoxLayout(self)
        content_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        self.code_drop_area = QPlainTextEdit()
        self.code_drop_area.setReadOnly(True)
        self.code_drop_area.setPlaceholderText("Drop a code file here")
        self.code_drop_area.setAcceptDrops(False)
        self.code_drop_area.setStyleSheet(LIGHT_DROP_AREA)
        self.code_drop_area.setFrameStyle(QFrame.NoFrame)

        self.shuffle_btn = QPushButton("  Shuffle")
        self.shuffle_btn.setIcon(QIcon(resource_path(os.path.join(ICON_PATH, "gears.png"))))
        self.shuffle_btn.setIconSize(QSize(16, 16))

        left_layout.addWidget(Section("Original Code", self.code_drop_area, dark_body=False))
        left_layout.addWidget(self.shuffle_btn)
        self.code_preview = QTextEdit()
        self.code_preview.setReadOnly(True)
        self.code_preview.setStyleSheet(LIGHT_TEXTEDIT)

        self.answer_choices = QTreeWidget()
        self.answer_choices.setColumnCount(2)
        self.answer_choices.setHeaderLabels(["Sequence", "Score"])
        self.answer_choices.setRootIsDecorated(True)
        self.answer_choices.setIndentation(12)

        self.init_answer_placeholders()
        self.answer_choices.setStyleSheet(ANSWER_LIST_STYLE)

        self.download_btn = QPushButton("  Download PNG")
        self.download_btn.setIcon(QIcon(resource_path(os.path.join(ICON_PATH, "download.png"))))
        self.download_btn.setIconSize(QSize(16, 16))

        right_layout.addWidget(Section("Shuffled Code", self.code_preview))
        right_layout.addWidget(Section("Answer Choices", self.answer_choices))
        right_layout.addWidget(self.download_btn)
        content_layout.addLayout(left_layout, 1)
        content_layout.addLayout(right_layout, 1)
        layout.addLayout(content_layout)
        self.setLayout(layout)

    def init_events(self):
        self.shuffle_btn.clicked.connect(self.shuffle_code)
        self.download_btn.clicked.connect(self.download_png)

    def handle_file_drop(self, file_path: str):
        if os.path.isfile(file_path):
            self.load_file(file_path)

    def on_drag_enter(self):
        self.code_drop_area.setStyleSheet(LIGHT_DROP_AREA_HIGHLIGHT)

    def on_drag_leave(self):
        self.code_drop_area.setStyleSheet(LIGHT_DROP_AREA)

    def load_file(self, file_path):
        filename = os.path.basename(file_path)
        self.filename = filename
        cache_path = os.path.join(BASE_PATH, "inputs")
        save_path = os.path.join(cache_path, filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        try:
            with open(file_path, "rb") as src, open(save_path, "wb") as dst:
                dst.write(src.read())
        except Exception as e:
            QMessageBox.critical(self, "Error", f": {e}")
            self.current_file = None
            return
        self.current_file = CodeFile(save_path)

        try:
            self.current_file.load()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to parse file: {e}")
            self.current_file = None
            return

        with open(save_path, "r", encoding="utf-8") as f:
            code = f.read()

        self.code_drop_area.setPlainText(code)
        ext = os.path.splitext(filename)[1]
        lang = language_from_extension(ext)

        self.highlighter = GenericHighlighter(self.code_drop_area.document(), language=lang)
        self.code_drop_area.setStyleSheet(LIGHT_DROP_AREA_ACTIVE)

        if self.current_file.warning_msg:
            QMessageBox.warning(self, "Duplicate Keys Detected", self.current_file.warning_msg)

    def init_answer_placeholders(self):
        self.answer_choices.clear()

        letters = ["a", "b", "c", "d", "e", "f", "g"]

        for letter in letters[: settings.no_of_choices]:
            top_item = QTreeWidgetItem([f"{letter})", "0.0"])

            detail_item = QTreeWidgetItem(["", ""])
            top_item.addChild(detail_item)

            self.answer_choices.addTopLevelItem(top_item)
        self.answer_choices.resizeColumnToContents(0)

    def shuffle_code(self):
        if not self.current_file:
            QMessageBox.warning(self, "No File", "Please upload a file first.")
            return

        file = self.current_file

        correct_plus_wrong = incorrect_instructions(file.correct_sol, file.wrong_inst)
        shuffled = shuffle_sol(correct_plus_wrong)

        self.shuffled_question = shuffled
        self.code_preview.setPlainText("\n".join(shuffled))

        correct_answer, remain_lines = gen_correct_answer(file.correct_sol, shuffled)
        partials = generate_partials(
            len(file.wrong_inst_dict), shuffled, file.wrong_inst_dict, correct_answer
        )

        try:
            choices = gen_random_choices_wICinst(
                correct_answer, settings.no_of_choices, remain_lines
            )
        except ValueError as e:
            QMessageBox.critical(self, "Invalid Setting", str(e))
            return

        candidate_indices = [i for i, ch in enumerate(choices) if ch != correct_answer]
        num_replacements = min(len(partials), len(candidate_indices))

        if num_replacements > 0:
            replace_idx = random.sample(candidate_indices, num_replacements)
            for part, idx in zip(partials[:num_replacements], replace_idx):
                choices[idx] = part

        self.answer_choices.clear()
        letters = ["a", "b", "c", "d", "e", "f", "g"]

        scored = []
        for ch in choices:
            if ch == correct_answer:
                score = 1.0
            elif ch in partials:
                idx = partials.index(ch)
                score = max(0, 1 - 0.25 * (idx + 1))
            else:
                score = 0.0
            scored.append((ch, score))

        scored.sort(key=lambda x: x[1], reverse=True)

        for i, (choice, score) in enumerate(scored):
            sequence_text = f"{letters[i]}) {choice}"
            score_text = f"{score:.2f}"

            top_item = QTreeWidgetItem([sequence_text, score_text])
            if score == 1.0:
                font = top_item.font(0)
                font.setBold(True)
                top_item.setFont(0, font)
                top_item.setFont(1, font)
                green = QBrush(QColor("#2e7d32"))
                top_item.setForeground(0, green)
                top_item.setForeground(1, green)

                top_item.setExpanded(True)

            if score == 1.0:
                detail_text = "✔ Correct solution"
            elif score > 0.0:
                detail_text = "⚠ Partial credit"
            else:
                detail_text = "✖ Wrong answer"

            detail_item = QTreeWidgetItem([detail_text, ""])
            top_item.addChild(detail_item)

            self.answer_choices.addTopLevelItem(top_item)

        self.answer_choices.resizeColumnToContents(0)
        self.answer_choices.resizeColumnToContents(1)

    def download_png(self):
        if not self.code_preview.toPlainText():
            QMessageBox.warning(self, "No Code", "No shuffled code to download.")
            return

        lines = []
        for el in range(len(self.shuffled_question)):
            left, content = self.shuffled_question[el].split(")", 1)
            lines.append(left + ") " + content.strip())

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save as PNG", "shuffled_code.png", "PNG Files (*.png)"
        )
        if not file_path:
            return

        try:
            download_image(lines, file_path)
            QMessageBox.information(self, "Saved", f"Shuffled code saved to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()
