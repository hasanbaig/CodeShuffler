import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from codeshuffler.gui.main_window import MainWindow

if sys.platform == "darwin":  # macOS
    os.environ["QT_MAC_WANTS_LAYER"] = "1"

app = QApplication(sys.argv)
ICON_PATH = os.path.join("codeshuffler", "gui", "icons")
icon = QIcon(os.path.join(ICON_PATH, "codeshuffler-icon.png"))
QApplication.instance().setWindowIcon(icon)
app.setApplicationName("CodeShuffler")
app.setOrganizationName("CodeShuffler")
app.setApplicationDisplayName("CodeShuffler")

gui = MainWindow()
gui.show()
sys.exit(app.exec_())
