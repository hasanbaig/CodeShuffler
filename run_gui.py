from PyQt5.QtWidgets import QApplication

from codeshuffler.gui.interface import CodeShufflerGUI

app = QApplication([])
gui = CodeShufflerGUI()
gui.show()
app.exec_()
