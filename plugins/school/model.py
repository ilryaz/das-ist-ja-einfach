import uuid

class Notebook:
    def __init__(self):
        self.data = {}
        self.week_config = {"1": {
                "name": "Maths",
                "days": ["Mn", "Tu"],
                "target_minutes": 660
            },

            "2": {
                "name": "Physics",
                "days": ["Wd", "Th", "Fr"],
                "target_minutes": 660
            },

            "3": {
                "name": "CS",
                "days": ["Fr", "Sa", "Su"],
                "target_minutes": 660
            },

            "4": {
                "name": "German",
                "days": ["Mn", "Tu", "Wd", "Th", "Fr", "Su"],
                "target_minutes": 660
            },
        }


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