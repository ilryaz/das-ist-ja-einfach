from PySide6.QtWidgets import (QWidget, QLabel, QPushButton,
                               QVBoxLayout, QHBoxLayout, QProgressBar,
                               QCalendarWidget, QSplitter, QDialog,
                               QDialogButtonBox, QListWidget, QListWidgetItem,
                               QLineEdit)
from PySide6.QtCore import Qt, Signal
from .model import Notebook


class SubjectDialog(QDialog):
    def __init__(self, notebook, data=None):
        super().__init__()

        self.setWindowTitle("New subject")
        self.setFixedSize(350, 200)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.notebook = notebook

        # central widgets
        central_widget = QWidget()
        central_layout = QVBoxLayout()

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter a name")

        self.time_goal_edit = QLineEdit()
        self.time_goal_edit.setPlaceholderText("Enter time in hours")

        
        # central widgets / week buttons
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout()

        self.day_buttons = {}

        for day in ("Mn", "Tu", "Wd", "Th", "Fr", "Sa", "Su"):
            button = QPushButton(day)
            button.setCheckable(True)
            button.setFixedSize(40, 30)
            self.day_buttons[day] = button
            buttons_layout.addWidget(button)

        buttons_widget.setLayout(buttons_layout)

        # central widgets / setting up
        central_layout.addWidget(self.name_edit)
        central_layout.addWidget(buttons_widget)
        central_layout.addWidget(self.time_goal_edit)

        central_widget.setLayout(central_layout)

        # lower widgets        
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # finish setting up
        main_layout.addWidget(central_widget)
        main_layout.addWidget(self.button_box)

        if data:
            self.set_edit_mode_data(data)
            self.id = list(data.keys())[0]
        else:
            self.id = self.notebook.generate_subject_id()


    def get_days(self):
        return [day for day, btn in self.day_buttons.items() if btn.isChecked()]


    def return_data(self):
        name = self.name_edit.text().strip()
        if not name:
            return None
    
        target = self.time_goal_edit.text().strip()
        if not target.isdigit() or int(target) <= 0:
            return None

        return {self.id: {"name": name,
                          "days": self.get_days(),
                          "target_minutes": int(target) * 60}}
    
    
    def set_edit_mode_data(self, data):
        id = list(data.keys())[0]
        subject_data = data[id]

        self.name_edit.setText(subject_data["name"])

        for day in subject_data["days"]:
            button = self.day_buttons[day]
            button.setChecked(True)

        self.time_goal_edit.setText(str(subject_data["target_minutes"] // 60))


class SubjectItemWidget(QWidget):
    delete_requested = Signal(object)


    def __init__(self, notebook, data, item):
        super().__init__()

        self.data = data
        self.item = item
        self.notebook = notebook

        self.id = list(data)[0]

        # UI
        layout = QHBoxLayout(self)

        self.subject_name = QLabel(self.data[self.id]["name"])
        edit_button = QPushButton("Edit")
        edit_button.setFixedSize(40, 30)
        delete_button = QPushButton("❌")
        delete_button.setFixedSize(30, 30)

        edit_button.clicked.connect(self.on_edit_subject)
        delete_button.clicked.connect(self.on_delete_subject)

        layout.addWidget(self.subject_name)
        layout.addStretch()
        layout.addWidget(edit_button)
        layout.addWidget(delete_button)

    
    def on_edit_subject(self):
        dialog = SubjectDialog(self.notebook, self.data)

        if dialog.exec() == QDialog.Accepted:
            new_data = dialog.return_data()

            if not new_data:
                return None

            self.data = new_data
            self.item.setData(Qt.UserRole, new_data)

            new_name = self.data[self.id]["name"]
            self.subject_name.setText(new_name)
    

    def on_delete_subject(self):
        self.delete_requested.emit(self)
    

class WeekSettingsDialog(QDialog):
    def __init__(self, notebook, parent=None):
        super().__init__(parent)

        self.notebook = notebook

        self.setMinimumWidth(400)
        self.setMinimumHeight(500)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # upper & central part
        self.list_widget = QListWidget()

        # lower part
        lower_widget = QWidget()
        lower_layout = QHBoxLayout()

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_subject)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        lower_layout.addWidget(self.add_button)
        lower_layout.addWidget(self.button_box)

        lower_widget.setLayout(lower_layout)

        main_layout.addWidget(self.list_widget)
        main_layout.addWidget(lower_widget)

        for id in self.notebook.week_config.keys():
            subject_data = self.notebook.week_config[id]
            
            data = {}
            data[id] = subject_data

            self.add_subject_listwidget_item(data)



    def add_subject(self):
        dialog = SubjectDialog(self.notebook)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.return_data()
            
            if not isinstance(data, dict):
                return None

            self.add_subject_listwidget_item(data)


    def add_subject_listwidget_item(self, data):
        item = QListWidgetItem()
        widget = SubjectItemWidget(self.notebook, data, item)
        widget.delete_requested.connect(self.delete_item)
        item.setSizeHint(widget.sizeHint())

        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)

        item.setData(Qt.UserRole, data)


    def get_subjects(self):
        subjects = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            data = item.data(Qt.UserRole)
            subjects.append(data)
        return subjects


    def delete_item(self, widget):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if self.list_widget.itemWidget(item) is widget:
                self.list_widget.takeItem(i)
                break


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

        self.calender_settings = QPushButton("Settings")
        self.calender_settings.clicked.connect(self.open_calender_settings)

        self.calender = QCalendarWidget()
        self.calender.clicked.connect(self.rebuild_ui)

        upper_left_layout.addWidget(self.calender_settings)
        upper_left_layout.addWidget(self.calender)

        upper_left_widget = QWidget()
        upper_left_widget.setLayout(upper_left_layout)

        # upper-right widgets
        self.upper_right_layout = QVBoxLayout()

        date = self.calender.selectedDate().toPython()
        days_map = {0: "Mn", 1: "Tu", 2: "Wd", 3: "Th", 4: "Fr", 5: "Sa", 6: "Su"}
        current_day = days_map[date.weekday()]

        for id in self.notebook.week_config.keys():
            subject_data = self.notebook.week_config[id]
            if current_day in subject_data["days"]:
                self.upper_right_layout.addLayout(self.create_subject_block(id))

        upper_right_widget = QWidget()
        upper_right_widget.setLayout(self.upper_right_layout)

        # lower widgets
        self.lower_layout = QVBoxLayout()

        for id in self.notebook.week_config.keys():
            self.lower_layout.addWidget(self.create_weekly_progress_bar(id))

        lower_widget = QWidget()
        lower_widget.setLayout(self.lower_layout)

        # summing everything up together
        top_splitter.addWidget(upper_left_widget)
        top_splitter.addWidget(upper_right_widget)
        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(lower_widget)

        main_splitter.setSizes([400, 600])
        main_splitter.setStretchFactor(1, 1)

        main_layout.addWidget(main_splitter)


    def create_subject_block(self, id):
        layout = QHBoxLayout()
        
        label = QLabel(self.notebook.week_config[id]["name"])
        layout.addWidget(label)

        # buttons
        for time in self.notebook.time_buttons["time_buttons"]:
            time = int(time)
            hours = int(time // 60)
            minutes = int(time % 60)
            if hours and not minutes:
                button = QPushButton(f"+{hours} h")
            elif minutes and not hours:
                button = QPushButton(f"+{minutes} m")
            elif hours and minutes:
                button = QPushButton(f"+{hours} h {minutes} m")
            button.clicked.connect(lambda checked=False, t=time: self.handle_add_minutes(id, t))
            layout.addWidget(button)

        add_time_button = QPushButton("+")
        add_time_button.setFixedWidth(30)

        layout.addWidget(add_time_button)

        return layout
    

    def open_calender_settings(self):
        settings = WeekSettingsDialog(self.notebook, self)

        if settings.exec() == QDialog.Accepted:
            subjects = settings.get_subjects()

            self.notebook.week_config.clear()

            for subject in subjects:
                subject_id = list(subject.keys())[0]

                self.notebook.week_config[subject_id] = subject[subject_id]


            self.rebuild_ui()


    def handle_add_minutes(self, id, minutes):
        date = self.calender.selectedDate().toPython()
        self.notebook.add_minutes(minutes, date, id)

        self.update_progress_bar(id)


    def create_weekly_progress_bar(self, id):
        progress_bar = QProgressBar()

        progress_bar.setMinimum(0)

        self.progress_bars[id] = progress_bar

        self.update_progress_bar(id)
        
        return progress_bar
    
    
    def update_progress_bar(self, id):
        date = self.calender.selectedDate().toPython()
        
        current_value = self.notebook.progress(id, date)
        maximum = self.notebook.week_config[id]["target_minutes"]

        pbar = self.progress_bars[id]

        pbar.setMaximum(maximum)
        pbar.setValue(current_value)

        hours = int(current_value // 60)
        minutes = int(current_value % 60)
        if hours != 0 and minutes != 0:
            pbar.setFormat(f"{self.notebook.week_config[id]["name"]}: {hours} h {minutes} min / {maximum // 60} h")
        elif hours == 0:
            pbar.setFormat(f"{self.notebook.week_config[id]["name"]}: {minutes} min / {maximum // 60} h")
        else:
            pbar.setFormat(f"{self.notebook.week_config[id]["name"]}: {hours} h / {maximum // 60} h")



    def rebuild_ui(self):
        days_map = {0: "Mn", 1: "Tu", 2: "Wd", 3: "Th", 4: "Fr", 5: "Sa", 6: "Su"}
        date = self.calender.selectedDate().toPython()
        current_day = days_map[date.weekday()]

        self.clear_layout(self.upper_right_layout)
        self.clear_layout(self.lower_layout)

        self.progress_bars.clear()

        for id in self.notebook.week_config.keys():
            subject_data = self.notebook.week_config[id]
            if current_day in subject_data["days"]:
                subject_layout = self.create_subject_block(id)
                self.upper_right_layout.addLayout(subject_layout)

            progress_bar = self.create_weekly_progress_bar(id)
            self.lower_layout.addWidget(progress_bar)
    

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())