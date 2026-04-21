from PySide6.QtWidgets import (QWidget, QLabel, QPushButton,
                               QVBoxLayout, QHBoxLayout, QProgressBar,
                               QCalendarWidget, QSplitter, QDialog,
                               QDialogButtonBox, QListWidget, QListWidgetItem,
                               QInputDialog)
from PySide6.QtCore import Qt
from .model import Notebook

class NewSubjectDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("New subject")
        self.setFixedSize(250, 300)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # lower widgets        
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        main_layout.addWidget(self.button_box)



class WeekSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumWidth(400)
        self.setMinimumHeight(250)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # upper & central part
        self.list_widget = QListWidget()

        # lower part
        lower_widget = QWidget()
        lower_layout = QHBoxLayout()

        self.add_button = QPushButton('Add')
        self.add_button.clicked.connect(self.add_subject)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        lower_layout.addWidget(self.add_button)
        lower_layout.addWidget(self.button_box)

        lower_widget.setLayout(lower_layout)

        main_layout.addWidget(self.list_widget)
        main_layout.addWidget(lower_widget)

    def add_subject(self):
        add_dialog = NewSubjectDialog()
        add_dialog.exec()






class SchoolPage(QWidget):
    def __init__(self):
        super().__init__()

        self.notebook = Notebook()
        self.progress_bars = {}

        main_layout = QVBoxLayout(self)
        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.setChildrenCollapsible(False)

        # upper part
        top_splitter = QSplitter(Qt.Horizontal)
        top_splitter.setChildrenCollapsible(False)

        # upper-left widgets
        upper_left_layout = QVBoxLayout()

        self.calender_settings = QPushButton('Settings')
        self.calender_settings.clicked.connect(self.open_calender_settings)

        self.calender = QCalendarWidget()

        upper_left_layout.addWidget(self.calender_settings)
        upper_left_layout.addWidget(self.calender)

        upper_left_widget = QWidget()
        upper_left_widget.setLayout(upper_left_layout)

        # upper-right widgets
        upper_right_layout = QVBoxLayout()

        for subject in self.notebook.week_config:
            upper_right_layout.addLayout(self.create_subject_block(subject))

        upper_right_widget = QWidget()
        upper_right_widget.setLayout(upper_right_layout)

        # lower widgets
        lower_layout = QVBoxLayout()

        for subject in self.notebook.week_config.keys():
            lower_layout.addWidget(self.create_weekly_progress_bar(subject))

        lower_widget = QWidget()
        lower_widget.setLayout(lower_layout)

        # summing everything up together
        top_splitter.addWidget(upper_left_widget)
        top_splitter.addWidget(upper_right_widget)
        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(lower_widget)
        main_layout.addWidget(main_splitter)

    def create_subject_block(self, subject):
        layout = QHBoxLayout()
        
        label = QLabel(subject)
        
        # buttons
        add_one_hour = QPushButton('+1 hour')
        add_thirty_minutes = QPushButton('+30 mins')
        add_fifteen_minutes = QPushButton('+15 mins')

        add_one_hour.clicked.connect(lambda: self.handle_add_hours(subject, 1))
        add_thirty_minutes.clicked.connect(lambda: self.handle_add_hours(subject, 0.5))
        add_fifteen_minutes.clicked.connect(lambda: self.handle_add_hours(subject, 0.25))

        layout.addWidget(label)
        layout.addWidget(add_one_hour)
        layout.addWidget(add_thirty_minutes)
        layout.addWidget(add_fifteen_minutes)

        return layout
    
    def handle_add_hours(self, subject, hours):
        date = self.calender.selectedDate().toPython()
        self.notebooks[subject].add_hours(hours, date)
        self.progress_bars[subject].setValue(self.notebooks[subject].progress(date))


        print(subject, hours, '\n') # откладка
    
    def create_weekly_progress_bar(self, subject):
        date = self.calender.selectedDate().toPython()

        progress_bar = QProgressBar()

        progress_bar.setMinimum(0)
        progress_bar.setMaximum(self.notebooks[subject].target_hours)
        
        progress_bar.setFormat(f"{subject}: %v / %m")

        current_value = self.notebooks[subject].progress(date)
        progress_bar.setValue(current_value)

        self.progress_bars[subject] = progress_bar
        
        return progress_bar
    
    def open_calender_settings(self):
        settings = WeekSettingsDialog(self)

        if settings.exec() == QDialog.Accepted:
            pass