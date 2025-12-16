from PyQt5.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from codeshuffler.gui.utils.dragdrop import FileDropHandler
from codeshuffler.gui.utils.styles import DARK_DROP_AREA, DARK_TEXTEDIT_HIGHLIGHT
from codeshuffler.lib.parser import create_exam_docx, parse_exam, shuffle_answers, shuffle_questions


class ExamShufflerTab(QWidget, FileDropHandler):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.exam_dict = None
        self.exam_file_path = None
        self.template_path = "codeshuffler/codefiles/templates/CodeShufflersTemplate.docx"

        self.init_ui()
        self.init_events()

        self.enable_file_drop(self, self._handle_exam_drop)

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.exam_drop_area = QPlainTextEdit()
        self.exam_drop_area.setReadOnly(True)
        self.exam_drop_area.setPlaceholderText("Drop a .docx exam file here...")
        self.exam_drop_area.setStyleSheet(DARK_DROP_AREA)
        layout.addWidget(self.exam_drop_area)

        button_row = QHBoxLayout()
        self.btn_shuffle_q = QPushButton("Shuffle Questions")
        self.btn_shuffle_a = QPushButton("Shuffle Answers")
        self.btn_shuffle_both = QPushButton("Shuffle Both")
        button_row.addWidget(self.btn_shuffle_q)
        button_row.addWidget(self.btn_shuffle_a)
        button_row.addWidget(self.btn_shuffle_both)
        layout.addLayout(button_row)

        self.save_exam_btn = QPushButton("Save Shuffled Exam")
        self.save_exam_answers_btn = QPushButton("Save Shuffled Exam + Answer Key")

        self.save_exam_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.save_exam_answers_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        save_row = QHBoxLayout()
        save_row.addWidget(self.save_exam_btn)
        save_row.addWidget(self.save_exam_answers_btn)

        layout.addLayout(save_row)

        self.setLayout(layout)

    def init_events(self):
        self.btn_shuffle_q.clicked.connect(self.shuffle_q)
        self.btn_shuffle_a.clicked.connect(self.shuffle_a)
        self.btn_shuffle_both.clicked.connect(self.shuffle_both)
        self.save_exam_btn.clicked.connect(self.save_exam)
        self.save_exam_answers_btn.clicked.connect(self.save_exam_with_answers)

    def on_drag_enter(self):
        self.exam_drop_area.setStyleSheet(DARK_TEXTEDIT_HIGHLIGHT)

    def on_drag_leave(self):
        self.exam_drop_area.setStyleSheet(DARK_DROP_AREA)

    def _handle_exam_drop(self, file_path):
        if not file_path.lower().endswith(".docx"):
            QMessageBox.warning(self, "Invalid File", "Please upload a .docx exam.")
            return

        try:
            self.exam_file_path = file_path
            self.exam_dict = parse_exam(file_path)

            self.exam_drop_area.setStyleSheet(DARK_DROP_AREA)
            self.exam_drop_area.setPlainText(
                f"Loaded exam: {file_path}\n\nFound {len(self.exam_dict)} questions."
            )

        except Exception as e:
            QMessageBox.critical(self, "Parsing Error", str(e))

    def shuffle_q(self):
        if not self.check_loaded():
            return
        self.exam_dict = shuffle_questions(self.exam_dict)
        self.exam_drop_area.appendPlainText("\nQuestions shuffled.")

    def shuffle_a(self):
        if not self.check_loaded():
            return
        self.exam_dict = shuffle_answers(self.exam_dict)
        self.exam_drop_area.appendPlainText("\nAnswers shuffled.")

    def shuffle_both(self):
        if not self.check_loaded():
            return
        self.exam_dict = shuffle_answers(shuffle_questions(self.exam_dict))
        self.exam_drop_area.appendPlainText("\nQuestions + Answers shuffled.")

    def save_exam(self):
        if not self.check_loaded():
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Shuffled Exam", "shuffled_exam.docx", "Word Documents (*.docx)"
        )

        if not save_path:
            return

        try:
            create_exam_docx(self.template_path, self.exam_dict, save_path)
            QMessageBox.information(self, "Saved", f"Shuffled exam saved to:\n{save_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error Saving", str(e))

    def save_exam_with_answers(self):
        if not self.check_loaded():
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Exam + Answer Key", "shuffled_exam_answers.docx", "Word Documents (*.docx)"
        )

        if not save_path:
            return

        try:
            create_exam_docx(self.template_path, self.exam_dict, save_path, answer_key=True)

            QMessageBox.information(self, "Saved", f"Exam saved to:\n{save_path}\n")

        except Exception as e:
            QMessageBox.critical(self, "Error Saving", str(e))

    def check_loaded(self):
        if not self.exam_dict:
            QMessageBox.warning(self, "No Exam Loaded", "Please upload a .docx exam first.")
            return False
        return True
