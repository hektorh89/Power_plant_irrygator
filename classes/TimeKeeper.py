import datetime


class TimeKeeper:

    def __init__(self, start_time, pump_nr):
        self.start_time = start_time
        self.current_time = None
        self.time_last_watered = None
        self.pump_nr = pump_nr

    def set_current_time(self, updated_time):
        self.current_time = updated_time

    def set_time_last_watered(self, updated_time):
        self.time_last_watered = updated_time

    @staticmethod
    def get_current_time():
        now = datetime.datetime.now()
        return now.strftime("%H:%M:%S")
