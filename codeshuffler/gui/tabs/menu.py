import sys

from PyQt5.QtWidgets import QAction, QMessageBox

from codeshuffler.gui.utils.styles import MENU_BAR_STYLE


def build_menu(main_window):
    menu_bar = main_window.menuBar()
    menu_bar.setStyleSheet(MENU_BAR_STYLE)

    if sys.platform == "darwin":
        file_menu = menu_bar.addMenu("CodeShuffler")
    else:
        file_menu = menu_bar.addMenu("&File")

    about_action = QAction("About CodeShuffler", main_window)
    about_action.setMenuRole(QAction.AboutRole)
    about_action.triggered.connect(
        lambda: QMessageBox.information(
            main_window,
            "About CodeShuffler",
            "CodeShuffler v1.0\nA code randomization and visualization tool.",
        )
    )

    settings_action = QAction("Settings...", main_window)
    settings_action.setMenuRole(QAction.PreferencesRole)
    settings_action.triggered.connect(main_window.open_settings)

    clear_cache_action = QAction("Clear Image Cache", main_window)
    clear_cache_action.triggered.connect(main_window.clear_image_cache)

    quit_action = QAction("Quit CodeShuffler", main_window)
    quit_action.setMenuRole(QAction.QuitRole)
    quit_action.triggered.connect(main_window.quit_codeshuffler)

    file_menu.addAction(about_action)
    file_menu.addAction(settings_action)

    file_menu.addSeparator()
    file_menu.addAction(clear_cache_action)

    file_menu.addSeparator()
    file_menu.addAction(quit_action)

    return menu_bar
