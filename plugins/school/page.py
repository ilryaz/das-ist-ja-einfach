from PySide6.QtWidgets import (QWidget, QLabel, QPushButton,
                               QVBoxLayout, QHBoxLayout, QLineEdit,
                               QFrame, QCalendarWidget)

from .model import Notebook


class SchoolPage(QWidget):
    def __init__(self):
        super().__init__()

        self.notebook = Notebook("Exam preparation", 30)

        main_layout = QVBoxLayout(self)

        upper_layout = QHBoxLayout()

        # upper-left widgets
        upper_left_layout = QVBoxLayout()

        calender = QCalendarWidget()
        upper_left_layout.addWidget(calender)

        # upper-right widgets
        upper_right_layout = QVBoxLayout()

        upper_right_layout.addLayout(self.create_subject_block('Mathematics'))
        upper_right_layout.addLayout(self.create_subject_block('German'))

        # lower widgets
        lower_layout = QVBoxLayout()

        lower_layout.addWidget(QLabel('me just a placeholder\nme just a placeholder\nme just a placeholder\nme just a placeholder\n'))

        upper_layout.addLayout(upper_left_layout)
        upper_layout.addLayout(upper_right_layout)
        main_layout.addLayout(upper_layout)
        main_layout.addLayout(lower_layout)

        

    def create_subject_block(self, name):
        label = QLabel(name)
    
        input_field = QLineEdit()
        input_field.setPlaceholderText("Write here")
        input_field.setFixedWidth(100)


        lower_layout = QHBoxLayout()
        lower_layout.addWidget(input_field)
        lower_layout.addStretch()

        block_layout = QVBoxLayout()
        block_layout.addWidget(label)
        block_layout.addLayout(lower_layout)

        return block_layout
