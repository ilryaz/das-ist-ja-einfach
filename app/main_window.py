import json
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QLabel, QSplitter,
                               QPushButton, QWidget,
                               QHBoxLayout, QListWidget, QStackedWidget,
                               QDialog, QVBoxLayout, QComboBox,
                               QDialogButtonBox, QApplication)
from plugins.school.plugin import SchoolPlugin

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setFixedSize(350, 200)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Theme button
        theme_button = QWidget()
        theme_layout = QHBoxLayout(theme_button)

        label = QLabel("Theme")

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "Catppuccin"])

        theme_layout.addWidget(label)
        theme_layout.addStretch()
        theme_layout.addWidget(self.theme_combo)

        # Lower buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Summing everything up together
        main_layout.addWidget(theme_button)
        main_layout.addWidget(self.button_box)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Productivity App")

        central_widget = QWidget()
        main_layout = QHBoxLayout()

        # Settings
        settings = QWidget()
        settings_layout = QVBoxLayout(settings)
        settings.setFixedWidth(50)

        settings_button = QPushButton("⚙️")
        settings_button.clicked.connect(self.open_settings_dialog)

        settings_layout.addStretch()
        settings_layout.addWidget(settings_button)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(90)

        # Stack
        self.stack = QStackedWidget()

        plugin = SchoolPlugin()

        page = plugin.create_page()

        self.sidebar.addItem(plugin.name)
        self.stack.addWidget(page)

        self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)

        # Splitters
        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.stack)
        splitter.setSizes([150, 800])
        splitter.setStretchFactor(1, 1)

        # Summing everything up together
        main_layout.addWidget(settings)
        main_layout.addWidget(splitter)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.load_theme()

    def open_settings_dialog(self):
        settings = SettingsDialog()

        if settings.exec() == QDialog.Accepted:
            theme = settings.theme_combo.currentText()

            self.save_theme(theme)
            self.apply_theme(theme)


    def save_theme(self, theme):
        SETTINGS_FILE = Path(__file__).parent.parent / "data" / "settings.json"

        data = {
            "theme": theme
        }

        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def apply_theme(self, theme):
        themes = {
            "Light": "light.qss",
            "Dark": "dark.qss",
            "Catppuccin": "catppuccin.qss"
        }

        theme_file = Path(__file__).parent.parent / "themes" / themes[theme]

        with open(theme_file, encoding="utf-8") as file:
            QApplication.instance().setStyleSheet(file.read())

    def load_theme(self):
        SETTINGS_FILE = Path(__file__).parent.parent / "data" / "settings.json"
        with open(SETTINGS_FILE, encoding="utf-8") as file:
            data = json.load(file)
            theme = data.get("theme", "Light")
        self.apply_theme(theme)