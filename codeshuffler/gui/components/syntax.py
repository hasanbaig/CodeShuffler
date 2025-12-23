import re

from PyQt5.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat


class GenericHighlighter(QSyntaxHighlighter):
    """Lightweight syntax highlighter that handles Python, C++, Java, and JS."""

    def __init__(self, document, language="python", *, dark_mode: bool = False):
        super().__init__(document)

        self.language = language.lower()
        self.dark_mode = dark_mode
        self.rules = []

        if self.dark_mode:
            keyword_color = QColor("#569CD6")
            string_color = QColor("#CE9178")
            comment_color = QColor("#6A9955")
            number_color = QColor("#B5CEA8")
            class_color = QColor("#4EC9B0")
            func_color = QColor("#DCDCAA")
        else:
            keyword_color = QColor("#0000AA")
            string_color = QColor("#A31515")
            comment_color = QColor("#008000")
            number_color = QColor("#098658")
            class_color = QColor("#267F99")
            func_color = QColor("#795E26")

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

        str_fmt = QTextCharFormat()
        str_fmt.setForeground(string_color)
        self.rules.append((re.compile(r"(['\"]).*?\1"), str_fmt))

        num_fmt = QTextCharFormat()
        num_fmt.setForeground(number_color)
        self.rules.append((re.compile(r"\b\d+\b"), num_fmt))

        com_fmt = QTextCharFormat()
        com_fmt.setForeground(comment_color)
        com_fmt.setFontItalic(True)

        if self.language == "python":
            self.rules.append((re.compile(r"#.*"), com_fmt))
        else:
            self.rules.append((re.compile(r"//.*"), com_fmt))
            self.rules.append((re.compile(r"/\*.*\*/"), com_fmt))

        class_fmt = QTextCharFormat()
        class_fmt.setForeground(class_color)
        class_fmt.setFontWeight(QFont.Bold)
        self.rules.append((re.compile(r"\bclass\s+\w+"), class_fmt))

        func_fmt = QTextCharFormat()
        func_fmt.setForeground(func_color)
        self.rules.append((re.compile(r"\bdef\s+\w+|\bfunction\s+\w+"), func_fmt))

    def highlightBlock(self, text: str):
        for pattern, fmt in self.rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, fmt)
