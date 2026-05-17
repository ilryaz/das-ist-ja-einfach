class Notebook:
    def __init__(self):
        self.data = {}
        self.week_config = {
            "Maths": {
                "days": ["Mn", "Tu"],
                "target_hours": 11
            },

            "Physics": {
                "days": ["Wd", "Fr"],
                "target_hours": 6
            },

            "CS": {
                "days": ["Mn", "Wd", "Fr", "Su"],
                "target_hours": 7
            },

            "German": {
                "days": ["Mn", "Tu", "Wd", "Th", "Fr", "Sa", "Su"],
                "target_hours": 7
            }
        }

    def add_hours(self, hours, date, subject):
        week = self.get_current_week(date)

        if week not in self.data:
            self.data[week] = {}

        self.data[week][subject] = self.data[week].get(subject, 0) + hours

        print(f"added {hours} hours to {week}, subject {subject} current: {self.data[week][subject]}")

    def progress(self, subject, date):
        week = self.get_current_week(date)

        if week not in self.data:
            return 0
        
        return self.data[week].get(subject, 0)
    
    def get_current_week(self, date):
        return f"{date.year}-W{date.isocalendar().week}"