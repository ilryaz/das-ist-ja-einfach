from datetime import date

class Notebook:
    def __init__(self, name, target_hours):
        self.name = name
        self.target_hours = target_hours

        self.data = {}

    def add_hours(self, hours, date):
        week = self.get_current_week(date)

        self.data[week] = self.data.setdefault(week, 0) + hours

        print(f'added {hours} hours to {week}\n{self.data[week]}')

    def progress(self, date):
        week = self.get_current_week(date)

        return self.data.get(week, 0)
    
    def get_current_week(self, date):
        return f"{date.year}-W{date.isocalendar().week}"