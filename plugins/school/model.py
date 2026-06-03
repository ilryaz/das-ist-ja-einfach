import uuid
import json
from pathlib import Path

class Notebook:
    def __init__(self):
        self.data = {}

        week_file = Path(__file__).parent.parent.parent / "data" / "school" / "week_config.json"
        with open(week_file, encoding="utf-8") as file:
            self.week_config = json.load(file)
        
        time_buttons_file = Path(__file__).parent.parent.parent / "data" / "school" / "time_buttons.json"
        with open(time_buttons_file, encoding="utf-8") as file:
            self.time_buttons = json.load(file)

    def add_minutes(self, minutes, date, id):
        week = self.get_current_week(date)

        if week not in self.data:
            self.data[week] = {}

        self.data[week][id] = self.data[week].get(id, 0) + minutes

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