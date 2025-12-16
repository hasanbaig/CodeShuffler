from __future__ import annotations

import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QActionGroup,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMenu,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from codeshuffler.gui.components.section import Section
from codeshuffler.gui.components.viewer import HtmlPreviewWidget
from codeshuffler.gui.utils.dragdrop import FileDropHandler
from codeshuffler.gui.utils.styles import LIGHT_DROP_AREA, LIGHT_DROP_AREA_HIGHLIGHT, LIGHT_TEXTEDIT
from codeshuffler.lib.parser import create_exam_docx, parse_exam, shuffle_answers, shuffle_questions
from codeshuffler.lib.preview import PreviewError, render_exam_html

ICON_PATH = os.path.join("codeshuffler", "gui", "icons")


class ExamShufflerTab(QWidget, FileDropHandler):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.exam_dict = None
        self.exam_file_path = None
        self.template_path = "codeshuffler/codefiles/templates/CodeShufflersTemplate.docx"

        self.shuffle_mode = "both"
        self.download_mode = "exam"

        self.init_ui()
        self.init_events()
        self.enable_file_drop(self, self.handle_file_drop)

    def init_ui(self):
        layout = QVBoxLayout(self)

        content = QHBoxLayout()
        left = QVBoxLayout()
        right = QVBoxLayout()

        self.exam_drop_area = QPlainTextEdit()
        self.exam_drop_area.setReadOnly(True)
        self.exam_drop_area.setPlaceholderText("Drop a .docx exam file here")
        self.exam_drop_area.setStyleSheet(LIGHT_DROP_AREA)
        self.exam_drop_area.setFrameStyle(QFrame.NoFrame)

        left.addWidget(Section("Exam Upload", self.exam_drop_area, dark_body=False))
        self.preview = HtmlPreviewWidget()
        self.preview.setStyleSheet(LIGHT_TEXTEDIT)

        right.addWidget(Section("Preview", self.preview), stretch=1)

        self.shuffle_btn = QToolButton()
        self.shuffle_btn.setPopupMode(QToolButton.MenuButtonPopup)

        shuffle_container = QWidget()
        shuffle_layout = QHBoxLayout(shuffle_container)
        shuffle_layout.setContentsMargins(0, 0, 20, 0)
        shuffle_layout.setSpacing(6)

        shuffle_icon = QLabel()
        shuffle_icon.setPixmap(QIcon(os.path.join(ICON_PATH, "gears.png")).pixmap(16, 16))
        shuffle_text = QLabel("Shuffle")

        shuffle_layout.addStretch()
        shuffle_layout.addWidget(shuffle_icon)
        shuffle_layout.addWidget(shuffle_text)
        shuffle_layout.addStretch()

        self.shuffle_btn.setLayout(shuffle_layout)

        self.shuffle_menu = QMenu(self)
        self.act_shuffle_both = self.shuffle_menu.addAction("Questions + Answers")
        self.act_shuffle_q = self.shuffle_menu.addAction("Questions only")
        self.act_shuffle_a = self.shuffle_menu.addAction("Answers only")
        self.shuffle_group = QActionGroup(self)
        self.shuffle_group.setExclusive(True)

        self.shuffle_group.addAction(self.act_shuffle_both)
        self.shuffle_group.addAction(self.act_shuffle_q)
        self.shuffle_group.addAction(self.act_shuffle_a)
        for act in (self.act_shuffle_both, self.act_shuffle_q, self.act_shuffle_a):
            act.setCheckable(True)
        self.act_shuffle_both.setChecked(True)

        self.shuffle_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.shuffle_btn.setMinimumWidth(160)

        temp_btn = QPushButton()
        default_height = temp_btn.sizeHint().height() + 1
        self.shuffle_btn.setFixedHeight(default_height)

        self.shuffle_btn.setMenu(self.shuffle_menu)
        self.shuffle_btn.clicked.connect(self.shuffle_exam)
        self.download_btn = QToolButton()
        self.download_btn.setPopupMode(QToolButton.MenuButtonPopup)

        download_container = QWidget()
        download_layout = QHBoxLayout(download_container)
        download_layout.setContentsMargins(0, 0, 20, 0)
        download_layout.setSpacing(6)

        download_icon = QLabel()
        download_icon.setPixmap(QIcon(os.path.join(ICON_PATH, "download.png")).pixmap(16, 16))
        download_text = QLabel("Download Exam")

        download_layout.addStretch()
        download_layout.addWidget(download_icon)
        download_layout.addWidget(download_text)
        download_layout.addStretch()

        self.download_btn.setLayout(download_layout)

        self.download_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.download_btn.setMinimumWidth(180)
        self.download_btn.setFixedHeight(default_height)

        self.download_menu = QMenu(self)
        self.act_dl_exam = self.download_menu.addAction("Exam only")
        self.act_dl_exam_key = self.download_menu.addAction("Exam + Answer Key")
        self.download_group = QActionGroup(self)
        self.download_group.setExclusive(True)

        self.download_group.addAction(self.act_dl_exam)
        self.download_group.addAction(self.act_dl_exam_key)
        for act in (self.act_dl_exam, self.act_dl_exam_key):
            act.setCheckable(True)
        self.act_dl_exam.setChecked(True)

        self.download_btn.setMenu(self.download_menu)
        self.download_btn.clicked.connect(self.save_exam)

        left.addWidget(self.shuffle_btn)
        right.addWidget(self.download_btn)
        content.addLayout(left, 1)
        content.addLayout(right, 1)
        layout.addLayout(content)
        self.setLayout(layout)

    def init_events(self):
        self.act_shuffle_both.triggered.connect(lambda: self.set_shuffle_mode("both"))
        self.act_shuffle_q.triggered.connect(lambda: self.set_shuffle_mode("questions"))
        self.act_shuffle_a.triggered.connect(lambda: self.set_shuffle_mode("answers"))

        self.act_dl_exam.triggered.connect(lambda: self.set_download_mode("exam"))
        self.act_dl_exam_key.triggered.connect(lambda: self.set_download_mode("exam+key"))
        self.shuffle_btn.clicked.connect(self.shuffle_exam)
        self.download_btn.clicked.connect(self.save_exam)

    def on_drag_enter(self):
        self.exam_drop_area.setStyleSheet(LIGHT_DROP_AREA_HIGHLIGHT)

    def on_drag_leave(self):
        self.exam_drop_area.setStyleSheet(LIGHT_DROP_AREA)

    def handle_file_drop(self, file_path: str):
        if not file_path.lower().endswith(".docx"):
            QMessageBox.warning(self, "Invalid File", "Please upload a .docx exam.")
            return

        try:
            self.exam_file_path = file_path
            self.exam_dict = parse_exam(file_path)

            self.exam_drop_area.setPlainText(
                f"{file_path}\n\n{len(self.exam_dict)} questions loaded."
            )
            self.shuffle_mode = "both"
            self.update_preview()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def set_shuffle_mode(self, mode: str):
        self.shuffle_mode = mode

    def shuffle_exam(self):
        if not self.exam_dict:
            QMessageBox.warning(self, "No Exam", "Please upload an exam first.")
            return

        if self.shuffle_mode == "questions":
            self.exam_dict = shuffle_questions(self.exam_dict)
        elif self.shuffle_mode == "answers":
            self.exam_dict = shuffle_answers(self.exam_dict)
        else:
            self.exam_dict = shuffle_answers(shuffle_questions(self.exam_dict))

        self.update_preview()

    def set_download_mode(self, mode: str):
        self.download_mode = mode

    def save_exam(self):
        if not self.exam_dict:
            QMessageBox.warning(self, "No Exam", "Please upload an exam first.")
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Exam",
            "shuffled_exam.docx",
            "Word Documents (*.docx)",
        )
        if not save_path:
            return

        create_exam_docx(
            self.template_path,
            self.exam_dict,
            save_path,
            answer_key=(self.download_mode == "exam+key"),
        )

        QMessageBox.information(self, "Saved", f"Saved to:\n{save_path}")

    def update_preview(self):
        if not self.exam_dict:
            self.preview.set_message("Load an exam to preview it.")
            return
        try:
            html = render_exam_html(
                self.exam_dict,
                title="Exam Preview",
                subtitle=f"{len(self.exam_dict)} questions",
            ).html
            self.preview.set_html(html)
        except PreviewError as e:
            self.preview.set_message("Preview unavailable.")
            QMessageBox.warning(self, "Preview Error", str(e))
