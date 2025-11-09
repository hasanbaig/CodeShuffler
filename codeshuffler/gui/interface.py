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
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from codeshuffler.gui.settings import SettingsDialog
from codeshuffler.gui.syntax import GenericHighlighter
from codeshuffler.lib import settings
from codeshuffler.lib.generator import (
    gen_correct_answer,
    gen_random_choices_wICinst,
    generate_partials,
    incorrect_instructions,
)
from codeshuffler.lib.models.codefile import CodeFile
from codeshuffler.lib.utils import download_image, shuffle_sol

BASE_PATH = os.path.join(os.getcwd(), "codeshuffler", "gui", "codefiles")
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

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setAcceptDrops(True)

        main_layout = QVBoxLayout(central_widget)

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

        main_layout.addLayout(top_bar)
        main_layout.addLayout(content_layout)

        self.current_file = None
        self.filename = None
        self.shuffled_question = None

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
                color = QColor("#4CAF50")  # green
                score = 1.0
            elif choice in partial_options:
                color = QColor("#FFA500")  # orange
                swap_index = partial_options.index(choice)
                swaps = swap_index + 1
                score = max(0, 1 - 0.25 * swaps)
            else:
                color = QColor("#000000")  # black
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

        if not os.path.exists(BASE_PATH):
            QMessageBox.information(self, "Clear Cache", "No image cache found.")
            return

        deleted = 0
        for filename in os.listdir(BASE_PATH):
            file_path = os.path.join(BASE_PATH, filename)
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
