from collections import OrderedDict

from functools import lru_cache
from dateutil.parser import parse as datetimeparse
from util import format_time

cache = OrderedDict()


class TimeSlot:
    def __init__(self, start_time: str, end_time: str, credits: int):
        self.start_time = datetimeparse(start_time)
        self.end_time = datetimeparse(end_time)
        self.credits = credits

    @lru_cache(maxsize=1024)
    def overlaps(self, other_timeslot: 'TimeSlot') -> bool:
        return self.start_time <= other_timeslot.end_time and self.end_time >= other_timeslot.start_time

    def does_not_overlap(self, other_timeslot: 'TimeSlot') -> bool:
        return not self.overlaps(other_timeslot)

    def __str__(self):
        return "[{0} - {1}] {2} SKS".format(
            format_time(self.start_time),
            format_time(self.end_time),
            self.credits
        )
    pass


days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

time_and_credits = [
    ["07:30", "09:10", 2],
    ["10:00", "11:40", 2],
    ["13:30", "15:10", 2],
    ["14:20", "16:20", 2],
    ["07:30", "10:00", 3],
    ["10:10", "13:30", 3],
    ["13:35", "16:20", 3],
]

timeslots = []

for day in days:
    for time_and_credit in time_and_credits:
        timeslots.append(TimeSlot(
            start_time=f"{day} {time_and_credit[0]}",
            end_time=f"{day} {time_and_credit[1]}",
            credits=time_and_credit[2]
        ))
        pass
    pass
