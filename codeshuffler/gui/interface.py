import os
import re

from PyQt5.QtGui import (
    QColor,
    QDragEnterEvent,
    QDropEvent,
    QFont,
    QSyntaxHighlighter,
    QTextCharFormat,
)
from PyQt5.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPlainTextEdit,
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


class GenericHighlighter(QSyntaxHighlighter):
    """Lightweight syntax highlighter that handles Python, C++, Java, and JS."""

    def __init__(self, document, language="python"):
        super().__init__(document)
        self.language = language.lower()
        self.rules = []

        # color palette
        keyword_color = QColor("#569CD6")  # blue
        string_color = QColor("#CE9178")  # red/orange
        comment_color = QColor("#6A9955")  # green
        number_color = QColor("#B5CEA8")  # teal
        class_color = QColor("#4EC9B0")  # cyan
        func_color = QColor("#DCDCAA")  # yellowish
        # regex patterns
        python_keywords = r"\b(def|class|import|from|return|if|else|elif|for|while|try|except|as|with|lambda|yield|pass|break|continue|in|is|and|or|not|None|True|False)\b"
        cpp_keywords = r"\b(int|float|double|char|void|if|else|while|for|return|class|public|private|protected|include|using|namespace|new|delete|this)\b"
        js_keywords = r"\b(function|var|let|const|if|else|for|while|return|class|extends|new|import|export|from|try|catch|await|async)\b"
        java_keywords = r"\b(class|public|private|protected|void|int|float|double|new|this|if|else|while|for|try|catch|return|import|package|static|final|extends|implements)\b"

        lang_to_kw = {
            "python": python_keywords,
            "cpp": cpp_keywords,
            "c++": cpp_keywords,
            "js": js_keywords,
            "javascript": js_keywords,
            "java": java_keywords,
        }
        kw_fmt = QTextCharFormat()
        kw_fmt.setForeground(keyword_color)
        kw_fmt.setFontWeight(QFont.Bold)
        self.rules.append((re.compile(lang_to_kw.get(self.language, python_keywords)), kw_fmt))
        # strings
        str_fmt = QTextCharFormat()
        str_fmt.setForeground(string_color)
        self.rules.append((re.compile(r"(['\"]).*?\1"), str_fmt))
        # numbers
        num_fmt = QTextCharFormat()
        num_fmt.setForeground(number_color)
        self.rules.append((re.compile(r"\b[0-9]+\b"), num_fmt))
        # comments
        com_fmt = QTextCharFormat()
        com_fmt.setForeground(comment_color)
        com_fmt.setFontItalic(True)
        if self.language == "python":
            self.rules.append((re.compile(r"#.*"), com_fmt))
        else:
            self.rules.append((re.compile(r"//.*"), com_fmt))
            self.rules.append((re.compile(r"/\*.*\*/"), com_fmt))
        # class names
        class_fmt = QTextCharFormat()
        class_fmt.setForeground(class_color)
        class_fmt.setFontWeight(QFont.Bold)
        self.rules.append((re.compile(r"\bclass\s+\w+"), class_fmt))
        # function names
        func_fmt = QTextCharFormat()
        func_fmt.setForeground(func_color)
        self.rules.append((re.compile(r"\bdef\s+\w+|\bfunction\s+\w+"), func_fmt))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, fmt)


class CodeShufflerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeShuffler")
        self.setAcceptDrops(True)
        self.setGeometry(200, 100, 900, 600)

        main_layout = QHBoxLayout()
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
                border: 2px #aaa;
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

        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 3)

        self.setLayout(main_layout)
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
                border: 2px dashed #aaa;
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
        self.current_file = save_path

        with open(save_path, "r", encoding="utf-8") as f:
            code = f.read()
        self.code_drop_area.setPlainText(code)

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
                border: 2px dashed #555;
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
            if choice == correct_answer:
                label = f"{letters[i]}) {choice}  <-- Correct Answer"
            else:
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
