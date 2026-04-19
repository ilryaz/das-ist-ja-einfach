from PySide6.QtWidgets import (QWidget, QLabel, QPushButton,
                               QVBoxLayout, QHBoxLayout, QProgressBar,
                               QCalendarWidget, QSplitter)
from PySide6.QtCore import Qt
from .model import Notebook


class SchoolPage(QWidget):
    def __init__(self):
        super().__init__()

        self.notebooks = {"Mathematics": Notebook("Mathematics", 11),
                          "German": Notebook("German", 7)}

        main_layout = QVBoxLayout(self)
        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.setChildrenCollapsible(False)

        # upper part
        top_splitter = QSplitter(Qt.Horizontal)
        top_splitter.setChildrenCollapsible(False)

        # upper-left widgets
        upper_left_layout = QVBoxLayout()

        self.calender = QCalendarWidget()
        upper_left_layout.addWidget(self.calender)

        upper_left_widget = QWidget()
        upper_left_widget.setLayout(upper_left_layout)

        # upper-right widgets
        upper_right_layout = QVBoxLayout()

        upper_right_layout.addLayout(self.create_subject_block('Mathematics'))
        upper_right_layout.addLayout(self.create_subject_block('German'))

        upper_right_widget = QWidget()
        upper_right_widget.setLayout(upper_right_layout)

        # lower widgets
        lower_layout = QVBoxLayout()

        lower_layout.addWidget(self.create_weekly_progress_bar())
        lower_layout.addWidget(self.create_weekly_progress_bar())

        lower_widget = QWidget()
        lower_widget.setLayout(lower_layout)

        # summing everything up together
        top_splitter.addWidget(upper_left_widget)
        top_splitter.addWidget(upper_right_widget)
        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(lower_widget)
        main_layout.addWidget(main_splitter)

        

    def create_subject_block(self, name):
        layout = QHBoxLayout()
        
        label = QLabel(name)
        
        # buttons
        add_one_hour = QPushButton('+1 hour')
        add_thirty_minutes = QPushButton('+30 mins')
        add_fifteen_minutes = QPushButton('+15 mins')

        add_one_hour.clicked.connect(lambda: self.handle_add_hours(name, 1))
        add_thirty_minutes.clicked.connect(lambda: self.handle_add_hours(name, 0.5))
        add_fifteen_minutes.clicked.connect(lambda: self.handle_add_hours(name, 0.25))

        layout.addWidget(label)
        layout.addWidget(add_one_hour)
        layout.addWidget(add_thirty_minutes)
        layout.addWidget(add_fifteen_minutes)

        return layout
    
    def handle_add_hours(self, name, hours):
        date = self.calender.selectedDate().toPython()
        self.notebooks[name].add_hours(hours, date)

        print(name, hours) # откладка
    
    def create_weekly_progress_bar(self):
        progress_bar = QProgressBar()
        progress_bar.minimum, progress_bar.maximum = 0, 100
        return progress_bar