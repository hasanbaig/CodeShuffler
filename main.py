import os
import sys

from PyQt5.QtWidgets import QApplication

from codeshuffler.gui.main_window import MainWindow

if sys.platform == "darwin":  # macOS
    os.environ["QT_MAC_WANTS_LAYER"] = "1"

app = QApplication(sys.argv)

app.setApplicationName("CodeShuffler")
app.setOrganizationName("CodeShuffler")
app.setApplicationDisplayName("CodeShuffler")

gui = MainWindow()
gui.show()
sys.exit(app.exec_())
