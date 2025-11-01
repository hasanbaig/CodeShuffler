import os
import sys

from PyQt5.QtWidgets import QApplication

from codeshuffler.gui.interface import CodeShufflerGUI

if sys.platform == "darwin":  # macOS
    os.environ["QT_MAC_WANTS_LAYER"] = "1"

app = QApplication(sys.argv)

app.setApplicationName("CodeShuffler")
app.setOrganizationName("CodeShuffler")
app.setApplicationDisplayName("CodeShuffler")

gui = CodeShufflerGUI()
gui.show()
sys.exit(app.exec_())
