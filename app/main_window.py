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
    def __init__(self, current_theme):
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
        self.theme_combo.setCurrentText(current_theme)

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
        self.setMinimumWidth(1000)
        self.setMinimumHeight(550)

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        main_layout = QHBoxLayout()

        # Settings
        settings = QWidget()
        settings.setObjectName("settingsPanel")
        settings_layout = QVBoxLayout(settings)
        settings.setFixedWidth(67)

        settings_button = QPushButton("⚙️")
        settings_button.setObjectName("settingsButton")
        settings_button.clicked.connect(self.open_settings_dialog)

        settings_layout.addStretch()
        settings_layout.addWidget(settings_button)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setMinimumWidth(120)
        self.sidebar.setMaximumWidth(250)

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
        settings = SettingsDialog(self.get_current_theme())

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


    def apply_theme(self, theme_name):
        themes_dir = Path(__file__).parent.parent / "themes"

        theme_file = themes_dir / f"{theme_name.lower()}.json"
        template_file = themes_dir / "template.qss"

        with open(theme_file, encoding="utf-8") as file:
            colors = json.load(file)

        with open(template_file, encoding="utf-8") as file:
            stylesheet = file.read()

        for key, value in colors.items():
            stylesheet = stylesheet.replace(f"${key}", value)

        QApplication.instance().setStyleSheet(stylesheet)


    def load_theme(self):
        self.apply_theme(self.get_current_theme())

    
    def get_current_theme(self):
        SETTINGS_FILE = Path(__file__).parent.parent / "data" / "settings.json"
        with open(SETTINGS_FILE, encoding="utf-8") as file:
            data = json.load(file)
            theme = data.get("theme", "Light")
            return theme