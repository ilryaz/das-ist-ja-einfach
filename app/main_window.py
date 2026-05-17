import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QLabel, QSplitter,
                               QPushButton, QWidget,
                               QHBoxLayout, QListWidget, QStackedWidget)
from plugins.school.plugin import SchoolPlugin
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Productivity App")

        central_widget = QWidget()
        main_layout = QHBoxLayout()

        settings_panel = QWidget()
        settings_panel.setFixedWidth(30)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setMaximumWidth(300)
        self.sidebar.setMinimumWidth(85)

        # Stack
        self.stack = QStackedWidget()

        plugin = SchoolPlugin()

        page = plugin.create_page()

        self.sidebar.addItem(plugin.name)
        self.stack.addWidget(page)

        self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.stack)
        splitter.setSizes([150, 800])
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(settings_panel)
        main_layout.addWidget(splitter)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
