import uuid
import json
from pathlib import Path

class Notebook:
    def __init__(self):
        DATA_FILE = Path(__file__).parent.parent.parent / "data" / "school" / "data.json"
        with open(DATA_FILE, encoding="utf-8") as file:
            self.data = json.load(file)

        WEEK_FILE = Path(__file__).parent.parent.parent / "data" / "school" / "week_config.json"
        with open(WEEK_FILE, encoding="utf-8") as file:
            self.week_config = json.load(file)
        
        TIME_BUTTONS_FILE = Path(__file__).parent.parent.parent / "data" / "school" / "time_buttons.json"
        with open(TIME_BUTTONS_FILE, encoding="utf-8") as file:
            self.time_buttons = json.load(file)

    def add_minutes(self, minutes, date, id):
        week = self.get_current_week(date)
        DATA_FILE = Path(__file__).parent.parent.parent / "data" / "school" / "data.json"

        if week not in self.data:
            self.data[week] = {}

        self.data[week][id] = self.data[week].get(id, 0) + minutes

        with open(DATA_FILE, "w", encoding="utf-8") as file:
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