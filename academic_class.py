import timeslot
from course import Course
from department import Department
from instructor import Instructor
from room import Room


class AcademicClass:
    def __init__(self, id, department: Department, course: Course, room: Room, meeting_time: timeslot.TimeSlot,
                 instructor: Instructor):
        self.id = id
        self.department = department
        self.course = course
        self.room = room
        self.meeting_time = meeting_time
        self.instructor = instructor

    def clone(self):
        return AcademicClass(self.id, self.department, self.course, self.room, self.meeting_time, self.instructor)

    def __str__(self):
        return f"{self.id}-{self.department.name}-{self.course.name}-{self.meeting_time}"
