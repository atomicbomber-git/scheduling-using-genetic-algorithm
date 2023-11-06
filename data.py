from typing import List

import timeslot
from course import Course
from department import Department
from instructor import Instructor
from room import Room


class Data:
    def __init__(
            self,
            departments: List[Department],
            courses: List[Course],
            instructors: List[Instructor],
            rooms: List[Room],
            meeting_times: List[timeslot.TimeSlot]
    ):
        self.rooms = rooms
        self.departments = departments
        self.courses: courses
        self.instructors = instructors
        self.meeting_times = meeting_times
