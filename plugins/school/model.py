import uuid
import json
from pathlib import Path

class Notebook:
    def __init__(self):
        self.data_files_directory = Path(__file__).parent.parent.parent / "data" / "school"
        
        self.DATA_FILE = self.data_files_directory / "data.json"
        self.WEEK_FILE = self.data_files_directory / "week_config.json"
        self.TIME_BUTTONS_FILE = self.data_files_directory / "time_buttons.json"

        with open(self.DATA_FILE, encoding="utf-8") as file:
            self.data = json.load(file)

        with open(self.WEEK_FILE, encoding="utf-8") as file:
            self.week_config = json.load(file)
        
        with open(self.TIME_BUTTONS_FILE, encoding="utf-8") as file:
            self.time_buttons = json.load(file)


    def add_minutes(self, minutes, date, id):
        week = self.get_current_week(date)

        if week not in self.data:
            self.data[week] = {}

        self.data[week][id] = self.data[week].get(id, 0) + minutes

        with open(self.DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)

        print(f"added {minutes} minutes to {week}, id {id} current: {self.data[week][id]}")


    def progress(self, id, date):
        week = self.get_current_week(date)

        if week not in self.data:
            return 0
        
        return self.data[week].get(id, 0)
    

    def get_current_week(self, date):
        return f"{date.year}-W{date.isocalendar().week}"
    

    def generate_subject_id(self):
        return str(uuid.uuid4())