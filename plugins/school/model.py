class Notebook:
    def __init__(self):
        self.data = {}
        self.week_config = {
            "Maths": {
                "days": ["Mn", "Tu"],
                "target_minutes": 660
            },

            "Physics": {
                "days": ["Wd", "Fr"],
                "target_minutes": 420
            },

            "CS": {
                "days": ["Mn", "Wd", "Fr", "Su"],
                "target_minutes": 360
            },

            "German": {
                "days": ["Mn", "Tu", "Wd", "Th", "Fr", "Sa", "Su"],
                "target_minutes": 360
            }
        }

    def add_minutes(self, minutes, date, subject):
        week = self.get_current_week(date)

        if week not in self.data:
            self.data[week] = {}

        self.data[week][subject] = self.data[week].get(subject, 0) + minutes

        print(f"added {minutes} minutes to {week}, subject {subject} current: {self.data[week][subject]}")

    def progress(self, subject, date):
        week = self.get_current_week(date)

        if week not in self.data:
            return 0
        
        return self.data[week].get(subject, 0)
    
    def get_current_week(self, date):
        return f"{date.year}-W{date.isocalendar().week}"