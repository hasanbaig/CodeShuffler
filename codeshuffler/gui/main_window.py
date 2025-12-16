import os
import sys

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTabWidget

from codeshuffler.gui.components.settings import SettingsDialog
from codeshuffler.gui.tabs.codeshuffler import CodeShufflerTab
from codeshuffler.gui.tabs.examshuffler import ExamShufflerTab
from codeshuffler.gui.tabs.menu import build_menu
from codeshuffler.gui.utils.dragdrop import FileDropHandler
from codeshuffler.gui.utils.styles import TAB_STYLE


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeShuffler")
        self.setGeometry(200, 100, 1000, 700)

        build_menu(self)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(TAB_STYLE)
        self.setCentralWidget(self.tabs)

        # Code Shuffler
        self.code_tab = CodeShufflerTab()
        self.tabs.addTab(self.code_tab, "Code Shuffler")

        # Exam Shuffler
        self.exam_tab = ExamShufflerTab()
        self.tabs.addTab(self.exam_tab, "Exam Shuffler")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        active = self.tabs.currentWidget()
        if isinstance(active, FileDropHandler):
            active.dragEnterEvent(e)

    def dragLeaveEvent(self, e):
        active = self.tabs.currentWidget()
        if isinstance(active, FileDropHandler):
            active.dragLeaveEvent(e)

    def dropEvent(self, e):
        active = self.tabs.currentWidget()
        if isinstance(active, FileDropHandler):
            active.dropEvent(e)

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()

    def clear_image_cache(self):
        cache_folder = os.path.join(os.getcwd(), "codeshuffler", "gui", "cache", "inputs")

        if not os.path.exists(cache_folder):
            QMessageBox.information(self, "Clear Cache", "No image cache found.")
            return

        deleted = 0
        for filename in os.listdir(cache_folder):
            try:
                file_path = os.path.join(cache_folder, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted += 1
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete {filename}: {e}")

        QMessageBox.information(self, "Cache Cleared", f"Deleted {deleted} cached images.")

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
