import random
from typing import List, Optional

from academic_class import AcademicClass
from data import Data
import numpy as np
import csv


class Schedule:
    def to_renderable(self):
        output = ""
        for ac in self.academic_classes:
            st = ac.meeting_time.start_time
            et = ac.meeting_time.end_time
            output = output + "{} {}\n".format(str(ac.department), str(ac.room))
            output = output + st.strftime("%a") + "\n"
            output = output + st.strftime("%H:%M") + " - " + et.strftime("%H:%M") + "\n"
            output += "\n"
            pass
        return output

    def dump_csv(self, filename: str = 'output.csv'):
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Department', 'Room', 'Course', 'Start Time', 'End Time', 'Instructor'])

            for academic_class in self.academic_classes:
                st = academic_class.meeting_time.start_time
                et = academic_class.meeting_time.end_time

                csv_writer.writerow([
                    str(academic_class.department),
                    str(academic_class.room),
                    str(academic_class.course),
                    st.strftime('%Y/%m/%d %H:%M'),
                    et.strftime('%Y/%m/%d %H:%M'),
                    str(academic_class.instructor),
                ])

        pass

    def __str__(self):
        return "\n".join([str(x) for x in self.academic_classes])

    def __init__(self, id, data: Optional[Data] = None, academic_classes: Optional[List[AcademicClass]] = None,
                 fitness: Optional[float] = None):
        self.id = id
        self.academic_classes = []

        class_id_counter = 0

        if academic_classes is None:
            for department in data.departments:
                for course in department.courses:
                    self.academic_classes.append(
                        AcademicClass(
                            class_id_counter,
                            department,
                            course,
                            random.choice(data.rooms),
                            random.choice(data.meeting_times),
                            random.choice(course.instructors)
                        )
                    )
                    class_id_counter += 1
                    pass
                pass
        else:
            self.academic_classes = academic_classes

        if fitness is None:
            self.fitness = self.calculate_fitness()
        else:
            self.fitness = fitness

    def calculate_and_cache_fitness(self):
        self.fitness = self.calculate_fitness()

    def clone(self):
        return Schedule(id=self.id, academic_classes=[ac.clone() for ac in self.academic_classes], fitness=self.fitness)

    def calculate_fitness(self):
        total_conflicts = 0

        academic_class: AcademicClass
        for i, academic_class in enumerate(self.academic_classes):

            if academic_class.room.seating_capacity < academic_class.course.max_students:
                total_conflicts += 1

            if academic_class.department.is_laboratory and academic_class.room.seating_capacity < 30:
                total_conflicts += 1

            if academic_class.meeting_time.credits < academic_class.department.credits:
                total_conflicts += 1

            comp_academic_class: AcademicClass
            for j, comp_academic_class in enumerate(self.academic_classes):
                if j > i:
                    timeslot1 = academic_class.meeting_time
                    timeslot2 = comp_academic_class.meeting_time

                    if timeslot1.overlaps(timeslot2):
                        if academic_class.room.name == comp_academic_class.room.name:
                            total_conflicts += 1

                        if academic_class.instructor.id == comp_academic_class.instructor.id:
                            total_conflicts += 1
                        pass
                    pass
                pass
            pass
        return 1.0 / (1.0 * total_conflicts + 1.0)
