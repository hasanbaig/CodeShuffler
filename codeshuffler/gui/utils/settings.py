from PyQt5.QtWidgets import (
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from codeshuffler.settings import settings


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CodeShuffler Settings")
        self.setModal(True)
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        self.include_checkbox = QCheckBox("Include incorrect instructions to increase difficulty")
        self.include_checkbox.setChecked(settings.include_incorrect_instructions)
        layout.addWidget(self.include_checkbox)

        first_line_layout = QHBoxLayout()
        first_line_label = QLabel("Keep first same X lines in MCQ options:")
        self.first_line_spin = QSpinBox()
        self.first_line_spin.setRange(1, 20)
        self.first_line_spin.setValue(settings.first_same_X_lines_MCQ)
        first_line_layout.addWidget(first_line_label)
        first_line_layout.addWidget(self.first_line_spin)
        layout.addLayout(first_line_layout)

        choice_layout = QHBoxLayout()
        choice_label = QLabel("Number of multiple choice options:")
        self.choice_spin = QSpinBox()
        self.choice_spin.setRange(3, 7)
        self.choice_spin.setValue(settings.no_of_choices)
        choice_layout.addWidget(choice_label)
        choice_layout.addWidget(self.choice_spin)
        layout.addLayout(choice_layout)

        img_x_layout = QHBoxLayout()
        img_x_label = QLabel("Image X Dimension:")
        self.image_x_spin = QSpinBox()
        self.image_x_spin.setRange(100, 5000)
        self.image_x_spin.setValue(settings.image_x_dim)
        img_x_layout.addWidget(img_x_label)
        img_x_layout.addWidget(self.image_x_spin)
        layout.addLayout(img_x_layout)

        img_y_layout = QHBoxLayout()
        img_y_label = QLabel("Image Y Dimension:")
        self.image_y_spin = QSpinBox()
        self.image_y_spin.setRange(100, 5000)
        self.image_y_spin.setValue(settings.image_y_dim)
        img_y_layout.addWidget(img_y_label)
        img_y_layout.addWidget(self.image_y_spin)
        layout.addLayout(img_y_layout)

        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.save_settings)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

    def save_settings(self):
        settings.include_incorrect_instructions = self.include_checkbox.isChecked()
        settings.first_same_X_lines_MCQ = self.first_line_spin.value()
        settings.no_of_choices = self.choice_spin.value()
        settings.image_x_dim = self.image_x_spin.value()
        settings.image_y_dim = self.image_y_spin.value()

        # TODO: persist these settings to disk for later sessions

        QMessageBox.information(self, "Settings Saved", "Your settings have been updated.")
        self.accept()
