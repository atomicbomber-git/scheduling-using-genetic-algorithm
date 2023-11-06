from collections import OrderedDict

from dateutil.parser import parse as datetimeparse

cache = OrderedDict()


def intern_overlaps(t1: 'TimeSlot', t2: 'TimeSlot') -> bool:
    global cache
    key1 = (t1.start_time, t1.end_time, t2.start_time, t2.end_time)
    key2 = (t2.start_time, t2.end_time, t1.start_time, t1.end_time)

    if (key1 not in cache) and (key2 not in cache):
        result = t1.start_time <= t2.end_time and t1.end_time >= t2.start_time

        cache[key1] = result
        cache[key2] = result

    return cache[key1]


class TimeSlot:
    def __init__(self, start_time: str, end_time: str, credits: int):
        self.start_time = datetimeparse(start_time)
        self.end_time = datetimeparse(end_time)
        self.credits = credits

    def overlaps(self, other_timeslot: 'TimeSlot') -> bool:
        return intern_overlaps(self, other_timeslot)

    def does_not_overlap(self, other_timeslot: 'TimeSlot') -> bool:
        return not self.overlaps(other_timeslot)

    def __str__(self):
        return "{0}-{1}, {2} SKS".format(
            self.start_time.strftime("%A %H:%M"),
            self.end_time.strftime("%A %H:%M"),
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
