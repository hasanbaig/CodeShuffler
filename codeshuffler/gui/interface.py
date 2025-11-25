import os
import random
import sys

from PyQt5.QtGui import QColor, QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import (
    QAction,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from codeshuffler.gui.utils.settings import SettingsDialog
from codeshuffler.gui.utils.syntax import GenericHighlighter
from codeshuffler.lib.generator import (
    gen_correct_answer,
    gen_random_choices_wICinst,
    generate_partials,
    incorrect_instructions,
)
from codeshuffler.lib.parser import create_exam_docx, parse_exam, shuffle_answers, shuffle_questions
from codeshuffler.lib.utils import download_image, shuffle_sol
from codeshuffler.models.codefile import CodeFile
from codeshuffler.settings import settings

BASE_PATH = os.path.join(os.getcwd(), "codeshuffler", "gui", "cache")
os.makedirs(BASE_PATH, exist_ok=True)


class CodeShufflerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeShuffler")
        self.setGeometry(200, 100, 900, 600)

        menu_bar = self.menuBar()
        menu_bar.setStyleSheet(
            """
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
        )
        # check to see if we're on mac or windows, pyqt handles menubars differently on each os
        if sys.platform == "darwin":
            file_menu = menu_bar.addMenu("CodeShuffler")
        else:
            file_menu = menu_bar.addMenu("&File")

        about_action = QAction("About CodeShuffler", self)
        settings_action = QAction("Settings...", self)
        clear_cache_action = QAction("Clear Image Cache", self)
        quit_action = QAction("Quit CodeShuffler", self)

        about_action.setMenuRole(QAction.AboutRole)
        settings_action.setMenuRole(QAction.PreferencesRole)
        quit_action.setMenuRole(QAction.QuitRole)

        about_action.triggered.connect(
            lambda: QMessageBox.information(
                self,
                "About CodeShuffler",
                "CodeShuffler v1.0\nA code randomization and visualization tool.",
            )
        )
        settings_action.triggered.connect(self.open_settings)
        clear_cache_action.triggered.connect(self.clear_image_cache)
        quit_action.triggered.connect(self.quit_codeshuffler)

        file_menu.addAction(about_action)
        file_menu.addAction(settings_action)
        file_menu.addSeparator()
        file_menu.addAction(clear_cache_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # TAB 1: CodeShuffler
        self.code_tab = QWidget()
        self.tabs.addTab(self.code_tab, "CodeShuffler")
        code_tab_layout = QVBoxLayout(self.code_tab)

        self.exam_tab = QWidget()
        self.tabs.addTab(self.exam_tab, "Exam Shuffler")
        self.init_exam_tab()

        top_bar = QHBoxLayout()
        logo_label = QLabel()
        title_label = QLabel("CodeShuffler")
        title_label.setStyleSheet(
            """
            QLabel {
                color: #000000;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                padding: 5px 10px;
            }
        """
        )
        top_bar.addWidget(logo_label)
        top_bar.addWidget(title_label)
        top_bar.addStretch()

        content_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        self.drop_label = QLabel(
            "Drop code file here or click to browse\n(JS, TS, Python, Java, C++, etc.)"
        )

        self.code_drop_area = QPlainTextEdit()
        self.code_drop_area.setReadOnly(True)
        self.code_drop_area.setAcceptDrops(False)
        self.code_drop_area.setPlaceholderText("Drop a code file here or click below to browse...")
        self.code_drop_area.setStyleSheet(
            """
            QPlainTextEdit {
                border: 2px solid #aaa;
                border-radius: 8px;
                background-color: #1e1e1e;
                color: #dcdcdc;
                font-family: 'Source Code Pro', 'Consolas', monospace;
                font-size: 13px;
                padding: 10px;
            }
        """
        )

        self.shuffle_btn = QPushButton("Shuffle")
        self.shuffle_btn.clicked.connect(self.shuffle_code)

        self.settings_btn = QPushButton("Settings")
        self.settings_btn.clicked.connect(self.open_settings)

        left_layout.addWidget(QLabel("Original Code Preview"))
        left_layout.addWidget(self.code_drop_area)
        left_layout.addWidget(self.shuffle_btn)
        left_layout.addWidget(self.settings_btn)

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

        content_layout.addLayout(left_layout, 1)
        content_layout.addLayout(right_layout, 1)

        code_tab_layout.addLayout(top_bar)
        code_tab_layout.addLayout(content_layout)

        self.current_file = None
        self.filename = None
        self.shuffled_question = None
        self.template = "codeshuffler/codefiles/templates/CodeShufflersTemplate.docx"

    def init_exam_tab(self):
        layout = QVBoxLayout(self.exam_tab)

        title = QLabel("Exam Shuffler")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.exam_drop_area = QPlainTextEdit()
        self.exam_drop_area.setReadOnly(True)
        self.exam_drop_area.setPlaceholderText("Drop a .docx exam file here...")
        self.exam_drop_area.setStyleSheet(
            """
            QPlainTextEdit {
                border: 2px dashed #888;
                border-radius: 8px;
                background-color: #1e1e1e;
                color: #dcdcdc;
                padding: 10px;
                font-family: 'Source Code Pro';
            }
        """
        )

        layout.addWidget(self.exam_drop_area)
        self.exam_tab.setAcceptDrops(True)
        self.exam_tab.dragEnterEvent = self.exam_drag_enter
        self.exam_tab.dropEvent = self.exam_drop_event

        button_row = QHBoxLayout()

        self.btn_shuffle_q = QPushButton("Shuffle Questions")
        self.btn_shuffle_q.clicked.connect(self.exam_shuffle_questions)

        self.btn_shuffle_a = QPushButton("Shuffle Answers")
        self.btn_shuffle_a.clicked.connect(self.exam_shuffle_answers)

        self.btn_shuffle_both = QPushButton("Shuffle Both")
        self.btn_shuffle_both.clicked.connect(self.exam_shuffle_both)

        button_row.addWidget(self.btn_shuffle_q)
        button_row.addWidget(self.btn_shuffle_a)
        button_row.addWidget(self.btn_shuffle_both)

        layout.addLayout(button_row)

        self.save_exam_btn = QPushButton("Save Shuffled Exam")
        self.save_exam_btn.clicked.connect(self.save_exam_doc)
        layout.addWidget(self.save_exam_btn)

        self.exam_dict = None
        self.exam_file_path = None

    def exam_drag_enter(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def exam_drop_event(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(".docx"):
                self.exam_file_path = file_path
                self.exam_dict = parse_exam(file_path)
                self.exam_drop_area.setPlainText(
                    f"Loaded exam: {file_path}\n\nFound {len(self.exam_dict)} questions."
                )
            else:
                QMessageBox.warning(self, "Invalid File", "Please upload a .docx exam.")

    def exam_shuffle_questions(self):
        if not self.exam_dict:
            QMessageBox.warning(self, "No Exam", "Upload an exam first.")
            return
        self.exam_dict = shuffle_questions(self.exam_dict)
        self.exam_drop_area.appendPlainText("\nQuestions shuffled.")

    def exam_shuffle_answers(self):
        if not self.exam_dict:
            QMessageBox.warning(self, "No Exam", "Upload an exam first.")
            return
        self.exam_dict = shuffle_answers(self.exam_dict)
        self.exam_drop_area.appendPlainText("\nAnswers shuffled.")

    def exam_shuffle_both(self):
        if not self.exam_dict:
            QMessageBox.warning(self, "No Exam", "Upload an exam first.")
            return
        self.exam_dict = shuffle_answers(shuffle_questions(self.exam_dict))
        self.exam_drop_area.appendPlainText("\nQuestions + Answers shuffled.")

    def save_exam_doc(self):
        if not self.exam_dict:
            QMessageBox.warning(self, "No Exam", "No shuffled exam to save.")
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Shuffled Exam", "shuffled_exam.docx", "Word Documents (*.docx)"
        )

        if not save_path:
            return

        try:
            create_exam_docx(self.template, self.exam_dict, save_path)
            QMessageBox.information(self, "Saved", f"Shuffled exam saved to:\n{save_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error Saving", str(e))

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.code_drop_area.setStyleSheet(
                """
                QPlainTextEdit {
                    border: 2px solid #00bfff;
                    background-color: #1e1e1e;
                    color: #dcdcdc;
                    font-family: 'Source Code Pro', 'Consolas', monospace;
                    font-size: 13px;
                    padding: 10px;
                }
            """
            )

    def dragLeaveEvent(self, event):
        self.code_drop_area.setStyleSheet(
            """
            QPlainTextEdit {
                border: 2px solid #aaa;
                background-color: #1e1e1e;
                color: #dcdcdc;
                font-family: 'Source Code Pro', 'Consolas', monospace;
                font-size: 13px;
                padding: 10px;
            }
        """
        )

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                self.save_dropped_file(file_path)

    def save_dropped_file(self, file_path):
        filename = os.path.basename(file_path)
        self.filename = filename
        save_path = os.path.join(BASE_PATH, filename)
        print(f"Saving dropped file to: {save_path}")

        with open(file_path, "rb") as source, open(save_path, "wb") as dest:
            dest.write(source.read())
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

        if self.current_file.warning_msg:
            QMessageBox.warning(self, "Duplicate Keys Detected", self.current_file.warning_msg)
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in [".py"]:
            lang = "python"
        elif file_ext in [".cpp", ".cc", ".h", ".hpp"]:
            lang = "cpp"
        elif file_ext in [".java"]:
            lang = "java"
        elif file_ext in [".js", ".ts"]:
            lang = "javascript"
        else:
            lang = "python"  # fallback

        self.highlighter = GenericHighlighter(self.code_drop_area.document(), language=lang)

        self.code_drop_area.setStyleSheet(
            """
            QPlainTextEdit {
                border: 2px solid #555;
                border-radius: 8px;
                background-color: #1e1e1e;
                color: #dcdcdc;
                font-family: 'Source Code Pro', 'Consolas', monospace;
                font-size: 13px;
                padding: 10px;
            }
        """
        )

    def browse_file(self, event):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select code file", "", "All Files (*.*)")
        if file_path:
            self.save_dropped_file(file_path)

    def shuffle_code(self):
        if not self.current_file:
            QMessageBox.warning(self, "No File", "Please upload a file first.")
            return
        file = self.current_file
        correct_sol_w_incorrect = incorrect_instructions(file.correct_sol, file.wrong_inst)
        shuffled_code = shuffle_sol(correct_sol_w_incorrect)
        self.shuffled_question = shuffled_code
        formatted_code = "\n".join(shuffled_code)
        self.code_preview.setPlainText(formatted_code)

        # --- generate options ---
        correct_answer, remain_lines = gen_correct_answer(file.correct_sol, shuffled_code)

        partial_options = generate_partials(
            len(file.wrong_inst_dict), shuffled_code, file.wrong_inst_dict, correct_answer
        )
        try:
            random_choices = gen_random_choices_wICinst(
                correct_answer, settings.no_of_choices, remain_lines
            )
        except ValueError as e:
            QMessageBox.critical(self, "Invalid Setting", str(e))
            return
        num_partials = len(partial_options)
        if num_partials + 1 >= settings.no_of_choices:
            QMessageBox.warning(
                self,
                "Warning",
                "Number of partial options exceeds or equals number of choices. "
                "Some answers might be missing!",
            )

        candidate_indices = [
            i for i, choice in enumerate(random_choices) if choice != correct_answer
        ]
        num_replacements = min(num_partials, len(candidate_indices))

        if num_replacements > 0:
            replace_indices = random.sample(candidate_indices, num_replacements)
            for partial_choice, idx in zip(partial_options[:num_replacements], replace_indices):
                random_choices[idx] = partial_choice
        self.answer_choices.clear()
        letters = ["a", "b", "c", "d", "e", "f", "g"]

        scored_options = []

        for choice in random_choices:
            if choice == correct_answer:
                color = QColor("#4CAF50")
                score = 1.0
            elif choice in partial_options:
                color = QColor("#FFA500")
                swap_index = partial_options.index(choice)
                swaps = swap_index + 1
                score = max(0, 1 - 0.25 * swaps)
            else:
                color = QColor("#000000")
                score = 0.0
            scored_options.append((choice, color, score))
        scored_options.sort(key=lambda x: x[2], reverse=True)
        self.answer_choices.clear()
        letters = ["a", "b", "c", "d", "e", "f", "g"]
        for i, (choice, color, score) in enumerate(scored_options):
            item_text = f"{letters[i]}) {choice}  |  Score: {score:.2f}"
            item = QListWidgetItem(item_text)
            item.setForeground(color)
            self.answer_choices.addItem(item)

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
        dialog = SettingsDialog(self)
        dialog.exec_()

    def clear_image_cache(self):
        cache_folder = os.path.join(BASE_PATH, "inputs")
        if not os.path.exists(cache_folder):
            QMessageBox.information(self, "Clear Cache", "No image cache found.")
            return

        deleted = 0
        for filename in os.listdir(cache_folder):
            file_path = os.path.join(cache_folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted += 1
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete {filename}: {e}")

        QMessageBox.information(self, "Cache Cleared", f"Deleted {deleted} cached image(s).")

    def quit_codeshuffler(self):
        confirm = QMessageBox.question(
            self,
            "Quit CodeShuffler",
            "Are you sure you want to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            sys.exit(0)
