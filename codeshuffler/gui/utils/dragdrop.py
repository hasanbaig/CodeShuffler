from PyQt5.QtWidgets import QWidget


class FileDropHandler:
    def enable_file_drop(self, widget: QWidget, drop_callback):
        widget.setAcceptDrops(True)
        self._drop_target_widget = widget
        self._file_drop_callback = drop_callback

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            if hasattr(self, "on_drag_enter"):
                self.on_drag_enter()

    def dragLeaveEvent(self, event):
        if hasattr(self, "on_drag_leave"):
            self.on_drag_leave()

    def dropEvent(self, event):
        if not event.mimeData().hasUrls():
            return

        for url in event.mimeData().urls():
            local_path = url.toLocalFile()
            if local_path and hasattr(self, "_file_drop_callback"):
                self._file_drop_callback(local_path)

        if hasattr(self, "on_drag_leave"):
            self.on_drag_leave()
