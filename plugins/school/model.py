from datetime import date

class Notebook:
    def __init__(self, name, target_hours):
        self.name = name
        self.target_hours = target_hours

        self.data = {}

    def add_hours(self, hours, day):
        week = self.get_current_week(day)

        self.data[week] = self.data.setdefault(week, 0) + hours

        print(f'added {hours} hours to {week}\n{self.data[week]}')

    def progress(self):
        if self.target_hours == 0:
            return 100
        return (self.current_hours / self.target_hours) * 100
    
    def get_current_week(self, date):
        return f"{date.year}-W{date.isocalendar().week}"