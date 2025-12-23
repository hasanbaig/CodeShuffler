import os
import sys

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication

from codeshuffler.gui.main_window import MainWindow
from codeshuffler.lib.utils import resource_path

if sys.platform == "darwin":  # macOS
    os.environ["QT_MAC_WANTS_LAYER"] = "1"

app = QApplication(sys.argv)
ICON_BASE_PATH = os.path.join("codeshuffler", "gui", "icons")
ICON_PATH = os.path.join(ICON_BASE_PATH, "codeshuffler-icon.png")
icon = QIcon(resource_path(ICON_PATH))
font = QFont("Tahoma")
font.setPointSize(10)
app.setFont(font)
QApplication.instance().setWindowIcon(icon)
app.setApplicationName("CodeShuffler")
app.setOrganizationName("CodeShuffler")
app.setApplicationDisplayName("CodeShuffler")

gui = MainWindow()
gui.show()
sys.exit(app.exec_())
