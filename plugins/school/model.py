class Notebook:
    def __init__(self):
        self.data = {}
        self.week_config = {}

    def add_hours(self, hours, date, subject):
        week = self.get_current_week(date)

        self.data[week][subject]['current_hours'] = self.data.setdefault(week, 0) + hours

        print(f'added {hours} hours to {week}, subject {subject} current: {self.data[week][subject]['current_hours']}')

    def progress(self, subject, date):
        week = self.get_current_week(date)

        return self.data.get(week, 0)
    
    def get_current_week(self, date):
        return f"{date.year}-W{date.isocalendar().week}"