import copy
import streamlit as st
import pandas as pd
from typing import List
import random

data = None


class Room:
    def __init__(self, name, seating_capacity: int):
        self.name = name
        self.seating_capacity = seating_capacity

    def __str__(self):
        return f"{self.name} ({self.seating_capacity})"


class Department:
    def __init__(self, name, department_courses):
        self.name = name
        self.courses = department_courses

    def __str__(self):
        return f"{self.name}"


class MeetingTime:
    def __init__(self, meeting_time_id, name):
        self.id = meeting_time_id
        self.name = name

    def __str__(self):
        return f"{self.name}"


class Instructor:
    def __init__(self, instructor_id, name):
        self.id = instructor_id
        self.name = name

    def __str__(self):
        return f"[{self.id}] {self.name}"


# st.json(Population(10))


class Course:
    def __init__(self, name, instructors, max_students):
        self.max_students = max_students
        self.instructors = instructors
        self.name = name

    def __str__(self):
        return f"{self.name} ({self.max_students})"


class AcademicClass:
    def __init__(self, id, department: Department, course: Course, room: Room, meeting_time: MeetingTime,
                 instructor: Instructor):
        self.id = id
        self.department = department
        self.course = course
        self.room = room
        self.meeting_time = meeting_time
        self.instructor = instructor

    def __str__(self):
        return f"{self.id}-{self.department.name}-{self.course.name}-{self.meeting_time.id}"


class Data:
    def __init__(
            self,
            departments: List[Department],
            courses: List[Course],
            instructors: List[Instructor],
            rooms: List[Room],
            meeting_times: List[MeetingTime]
    ):
        self.rooms = rooms
        self.departments = departments
        self.courses: courses
        self.instructors = instructors
        self.meeting_times = meeting_times


class Schedule:
    def __str__(self):
        return "\n".join([str(x) for x in self.academic_classes])

    def __init__(self, id):
        self.id = id
        self.academic_classes: List[AcademicClass] = []

        class_id_counter = 0
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
        pass

    pass

    def calculate_fitness(self):
        total_conflicts = 0

        academic_class: AcademicClass
        for i, academic_class in enumerate(self.academic_classes):

            if academic_class.room.seating_capacity < academic_class.course.max_students:
                total_conflicts += 1

            comp_academic_class: AcademicClass
            for j, comp_academic_class in enumerate(self.academic_classes):
                if j >= i:
                    if academic_class.meeting_time.id == comp_academic_class.meeting_time.id and (
                            academic_class.id != comp_academic_class.id
                    ):
                        if academic_class.room.name == comp_academic_class.room.name:
                            total_conflicts += 1

                        if academic_class.instructor.id == comp_academic_class.instructor.id:
                            total_conflicts += 1
                    pass
                pass
            pass
        return 1.0 / (1.0 * total_conflicts + 1.0)


class Population:
    def __init__(self, pop_size):
        schedule_id_counter = 0
        self.schedules = []

        for _ in range(0, pop_size):
            self.schedules.append(Schedule(schedule_id_counter))
            schedule_id_counter += 1
            pass

        self.sort_schedules_by_fitness()

    def clone(self, source_data: Data):
        pop = Population(0)
        for self_schedule in self.schedules:
            pop.schedules.append(self_schedule)
        return pop

    def schedule_desc(self):
        return ", ".join([str(x.id) for x in self.schedules])

    def sort_schedules_by_fitness(self):
        self.schedules.sort(key=lambda x: x.calculate_fitness(), reverse=True)

    def average_fitness(self):
        return sum([schedule.calculate_fitness() for schedule in self.schedules]) / len(self.schedules)


class GeneticAlgo:
    def __init__(
            self,
            population_size: int,
            elite_schedules_count: int,
            tournament_size: int,
            mutation_rate: float
    ):
        self.population_size = population_size
        self.elite_schedules_count = elite_schedules_count
        self.tournament_size = tournament_size
        self.mutation_rate = mutation_rate
        pass

    def mutate_schedule(self, sche: Schedule) -> Schedule:
        new_schedule = Schedule(sche.id)

        for idx, academic_class in enumerate(sche.academic_classes):
            if self.mutation_rate <= random.random():
                new_schedule.academic_classes[idx] = academic_class

        return new_schedule

    def mutate_population(self, pop: Population):
        pop.sort_schedules_by_fitness()

        for idx in range(self.elite_schedules_count, len(pop.schedules)):
            pop.schedules[idx] = self.mutate_schedule(pop.schedules[idx])
            pass

        return pop

    def select_tournament_schedule(self, pop: Population) -> Schedule:
        random.seed()

        tournament_participants: List[Schedule] = random.sample(pop.schedules, self.tournament_size)
        tournament_participants.sort(key=lambda schedule: schedule.calculate_fitness(), reverse=True)
        winner = copy.deepcopy(tournament_participants[0])

        return winner

    def crossover_population(self, pop: Population):
        pop.sort_schedules_by_fitness()
        crossover_pop = Population(0)
        pop.sort_schedules_by_fitness()

        for idx in range(0, self.elite_schedules_count):
            crossover_pop.schedules.append(pop.schedules[idx])
            pass

#         st.text( f"PPPXX {pop.schedules[0].calculate_fitness()}")

        pop.sort_schedules_by_fitness()


        for _ in range(self.elite_schedules_count, self.population_size):
            parent_schedule_1 = self.select_tournament_schedule(pop)
            parent_schedule_2 = self.select_tournament_schedule(pop)

            child_schedule = self.get_schedule_by_crossover(parent_schedule_1, parent_schedule_2)
            crossover_pop.schedules.append(child_schedule)

#         st.text( f"PPPXXAS {pop.schedules[0].calculate_fitness()}")


        return crossover_pop

    def get_schedule_by_crossover(self, parent_schedule_1, parent_schedule_2):
        for idx, _ in enumerate(parent_schedule_1.academic_classes):
            if random.random() > 0.5:
                parent_schedule_1.academic_classes[idx] = copy.deepcopy(parent_schedule_2.academic_classes[idx])

        return parent_schedule_1

    def evolve_population(self, pop: Population) -> Population:
        population = self.mutate_population(self.crossover_population(pop))

        population.sort_schedules_by_fitness()
        return population

    pass


st.set_page_config(layout="wide")

st.title("Penjadwalan dengan Genetic Algorithm")

st.divider()

st.subheader("Pengaturan Data")

ID_FIELD = "ID"
INSTRUCTOR_NAMES_FIELD = "Nama Instruktur"
ROOM_CODE_FIELD = "Kode Ruangan"
STUDENT_CAPACITY_FIELD = "Kapasitas"
MEETING_TIME_NAME_FIELD = "Pertemuan"
COURSE_ID_FIELD = "CourseID"
INSTRUCTOR_KEY_FIELD = "Nama Instruktur FIELD"
STUDENT_AMOUNT_FIELD = "Jumlah Siswa"

DEPT_NAME_FIELD = "Department Name"
COURSE_NAMES_FIELD = "Course IDS"

raw_rooms = pd.DataFrame([
    ("R1", 20),
    ("R2", 20),
    ("R3", 20),
    ("R4", 30),
    ("R5", 30),
], columns=[ROOM_CODE_FIELD, STUDENT_CAPACITY_FIELD])

raw_meeting_times = pd.DataFrame([
    ("1", "SENIN W1"),
    ("2", "SENIN W2"),
    ("3", "SENIN W3"),
    ("4", "SENIN W4"),
    ("5", "SELASA W1"),
    ("6", "SELASA W2"),
    ("7", "SELASA W3"),
    ("8", "SELASA W4"),
    ("9", "RABU W1"),
    ("10", "RABU W2"),
    ("11", "RABU W3"),
    ("12", "RABU W4"),
    ("13", "KAMIS W1"),
    ("14", "KAMIS W2"),
    ("15", "KAMIS W3"),
    ("16", "KAMIS W4"),
    ("17", "JUMAT W1"),
    ("18", "JUMAT W2"),
    ("19", "JUMAT W3"),
    ("20", "JUMAT W4"),
], columns=[ID_FIELD, MEETING_TIME_NAME_FIELD])

raw_instructors = pd.DataFrame([
    (1, "ASRUL ABDULLAH , S.Kom, M.Cs"),
    (2, "BARRY CEASAR OCTARIADI , S.Kom., M.Cs"),
    (3, "ALDA CENDEKIA SIREGAR , S.Kom., M.Cs"),
    (4, "SUCIPTO , M.Kom"),
    (5, "SYARIFAH PUTRI AGUSTINI ALKADRI , ST,M.Kom"),
    (6, "RACHMAT WAHID SALEH INSANI , S.Kom, M.Cs"),
    (7, "NEDI SURYADI, M.T"),
    (8, "HERMANTO , S.Pd.I,M.Pd.I"),
    (9, "M. FAJRIN , S.H, M.H"),
    (10, "RYAN PERMANA, M.Pd"),
    (11, "RINI ELVRI , S.Ag., M.Pd."),
    (12, "DENY PRIMANDA, M.Eng"),
    (13, "ELIN B SOMANTRI , S.Ag, M.Pd"),
    (14, "YUNIARTI , S.Pd,M.Pd"),
], columns=[ID_FIELD, INSTRUCTOR_NAMES_FIELD])


def get_instructor_desc_by_index(index):
    row = raw_instructors.iloc[index]
    return get_inst_desc_by_tuple(row)


def get_inst_desc_by_tuple(row):
    return f"[{row[ID_FIELD]}] {row[INSTRUCTOR_NAMES_FIELD]}"


raw_courses = pd.DataFrame([
    ("course1", [get_instructor_desc_by_index(1)], 20),
    ("course2", [get_instructor_desc_by_index(2)], 20),
    ("course3", [get_instructor_desc_by_index(4)], 20),
    ("course4", [get_instructor_desc_by_index(8)], 20),
    ("course5", [get_instructor_desc_by_index(9)], 20),
    ("course6", [get_instructor_desc_by_index(0)], 30),
    ("course7", [get_instructor_desc_by_index(1)], 20),
    ("course8", [get_instructor_desc_by_index(0)], 30),
    ("course9", [get_instructor_desc_by_index(9)], 20),
    ("course10", [get_instructor_desc_by_index(0)], 30),
    ("course11", [get_instructor_desc_by_index(2)], 20),
    ("course12", [get_instructor_desc_by_index(3)], 30),
    ("course13", [get_instructor_desc_by_index(5)], 30),
    ("course14", [get_instructor_desc_by_index(6)], 20),
    ("course15", [get_instructor_desc_by_index(10)], 20),
    ("course16", [get_instructor_desc_by_index(0)], 30),
    ("course17", [get_instructor_desc_by_index(2)], 20),
    ("course18", [get_instructor_desc_by_index(3)], 30),
    ("course19", [get_instructor_desc_by_index(5)], 30),
    ("course20", [get_instructor_desc_by_index(6)], 20),
    ("course21", [get_instructor_desc_by_index(10)], 20),
    ("course22", [get_instructor_desc_by_index(0)], 30),
    ("course23", [get_instructor_desc_by_index(1)], 20),
    ("course24", [get_instructor_desc_by_index(2)], 20),
    ("course25", [get_instructor_desc_by_index(3)], 30),
    ("course26", [get_instructor_desc_by_index(5)], 30),
    ("course27", [get_instructor_desc_by_index(10)], 20),
    ("course28", [get_instructor_desc_by_index(1)], 20),
    ("course29", [get_instructor_desc_by_index(2)], 20),
    ("course30", [get_instructor_desc_by_index(3)], 30),
    ("course31", [get_instructor_desc_by_index(4)], 20),
    ("course32", [get_instructor_desc_by_index(6)], 20),
    ("course33", [get_instructor_desc_by_index(8)], 20),
    ("course34", [get_instructor_desc_by_index(12)], 20),
    ("course35", [get_instructor_desc_by_index(13)], 20),
    ("course36", [get_instructor_desc_by_index(1)], 20),
    ("course37", [get_instructor_desc_by_index(3)], 30),
    ("course38", [get_instructor_desc_by_index(4)], 20),
    ("course39", [get_instructor_desc_by_index(6)], 20),
    ("course40", [get_instructor_desc_by_index(11)], 20),
    ("course41", [get_instructor_desc_by_index(12)], 20),
    ("course42", [get_instructor_desc_by_index(13)], 20),
    ("course43", [get_instructor_desc_by_index(1)], 20),
    ("course44", [get_instructor_desc_by_index(3)], 30),
    ("course45", [get_instructor_desc_by_index(4)], 20),
    ("course46", [get_instructor_desc_by_index(6)], 20),
    ("course47", [get_instructor_desc_by_index(7)], 20),
    ("course48", [get_instructor_desc_by_index(8)], 20),
    ("course49", [get_instructor_desc_by_index(11)], 20),
    ("course50", [get_instructor_desc_by_index(13)], 20),
], columns=[COURSE_ID_FIELD, INSTRUCTOR_NAMES_FIELD, STUDENT_AMOUNT_FIELD])


def find_instructor_by_name(instructor_name, instructors_list: List[Instructor]):
    for instructor in instructors_list:
        if str(instructor) == instructor_name:
            return instructor
    return None


def raw_course_to_course(row, instructors: List[Instructor]):
    instructors = [find_instructor_by_name(instructor_name, instructors) for instructor_name in
                   row[INSTRUCTOR_NAMES_FIELD]]

    return Course(row[COURSE_ID_FIELD], instructors, row[STUDENT_AMOUNT_FIELD])


raw_departments = pd.DataFrame([
    ("PEMROGRAMAN BERBASIS KERANGKA KERJA", ["course6", "course8"]),
    ("JARINGAN KOMPUTER", ["course10", "course16", "course22"]),
    ("ALGORITMA GENETIKA", ["course1"]),
    ("SISTEM TEMU KEMBALI INFORMASI", ["course1"]),
    ("LOGIKA SAMAR", ["course1"]),
    ("KEAMANAN KOMPUTER", ["course7", "course5", "course9"]),
    ("METODE NUMERIK", ["course23", "course14", "course20"]),
    ("ARSITEKTUR DAN ORGANISASI KOMPUTER", ["course28", "course36", "course43"]),
    ("KECERDASAN BERKOLONI", ["course2"]),
    ("KECERDASAN BUATAN", ["course11", "course17", "course24"]),
    ("LOGIKA INFORMATIKA", ["course29", "course40", "course49"]),
    ("DESAIN PENGALAMAN PENGGUNA", ["course12", "course18", "course25"]),
    ("ALGORITMA DAN STRUKTUR DATA", ["course30", "course37", "course44"]),
    ("SISTEM PENDUKUNG KEPUTUSAN", ["course3"]),
    ("PENJAMINAN KUALITAS PERANGKAT LUNAK", ["course3"]),
    ("TEORI BAHASA DAN OTOMATA", ["course31", "course38", "course45"]),
    ("PEMROGRAMAN BERORIENTASI OBJEK", ["course13", "course19", "course26"]),
    ("PEMROGRAMAN WEB LANJUT", ["course13", "course19", "course26"]),
    ("ALJABAR LINEAR", ["course32", "course39", "course46"]),
    ("AIK 2 (IBADAH MUAMALAH DAN AKHLAK)", ["course47", "course41", "course34"]),
    ("PENDIDIKAN KEWARGANEGARAAN", ["course4", "course33", "course48"]),
    ("AIK 4 (ISLAM & ILMU PENGETAHUAN)", ["course27", "course21", "course15"]),
    ("ENGLISH FOR SPECIFIC PURPOSES", ["course35", "course42", "course50"]),
], columns=[DEPT_NAME_FIELD, COURSE_NAMES_FIELD])


def find_course_by_name(course_name, courses: List[Course]):
    for course in courses:
        if course.name == course_name:
            return course
    return None


def raw_dept_to_dept(row, courses: List[Course]):
    course_list = [find_course_by_name(course_name, courses) for course_name in row[COURSE_NAMES_FIELD]]
    return Department(row[DEPT_NAME_FIELD], course_list)


def get_data():
    instructors_list = raw_instructors.apply(lambda row: Instructor(row[ID_FIELD], row[INSTRUCTOR_NAMES_FIELD]),
                                             axis=1).to_list()
    plain_courses = (raw_courses.apply(lambda row: raw_course_to_course(row, instructors_list), axis=1)).to_list()

    plain_departments = (raw_departments.apply(lambda row: raw_dept_to_dept(row, plain_courses), axis=1)).to_list()
    return Data(
        departments=plain_departments,
        instructors=instructors_list,
        courses=plain_courses,
        rooms=(raw_rooms.apply(lambda row: Room(row[ROOM_CODE_FIELD], row[STUDENT_CAPACITY_FIELD]), axis=1)).to_list(),
        meeting_times=(
            raw_meeting_times.apply(lambda row: MeetingTime(row[ID_FIELD], row[MEETING_TIME_NAME_FIELD]),
                                    axis=1)).to_list()
    )


def convert_to_json_recursive(obj, depth=20):
    """
    Recursively converts a Python object to JSON with a specified recursion depth.

    Args:
        obj: The Python object to convert.
        depth: The maximum recursion depth (default is 10).

    Returns:
        A JSON representation of the input object.
    """
    if depth <= 0:
        return None

    if isinstance(obj, (int, float, bool, str, type(None))):
        return obj

    if isinstance(obj, list):
        return [convert_to_json_recursive(item, depth - 1) for item in obj]

    if isinstance(obj, dict):
        return {key: convert_to_json_recursive(value, depth - 1) for key, value in obj.items()}

    if hasattr(obj, "__dict__"):
        return convert_to_json_recursive(obj.__dict__, depth - 1)

    return str(obj)


POPULATION_SIZE = st.number_input("POPULATION_SIZE", value=9)
NUMB_OF_ELITE_SCHEDULES = st.number_input("NUMB_OF_ELITE_SCHEDULES", value=1)
TOURNAMENT_SELECTION_SIZE = st.number_input("TOURNAMENT_SELECTION_SIZE", value=3, min_value=0,
                                            max_value=POPULATION_SIZE)
MUTATION_RATE = st.number_input("MUTATION_RATE", value=0.1, min_value=0.0, max_value=1.0, step=0.1)


data = get_data()

if st.session_state.get("initial_pop") is None:
    st.session_state["initial_pop"] = Population(POPULATION_SIZE)

initial_pop = st.session_state["initial_pop"]

algo = GeneticAlgo(
    population_size=POPULATION_SIZE,
    elite_schedules_count=NUMB_OF_ELITE_SCHEDULES,
    tournament_size=TOURNAMENT_SELECTION_SIZE,
    mutation_rate=MUTATION_RATE
)

chart_data = []


def perform(pop: Population):
    pop = pop.clone(data)
    idx = 0
    while True:
        pop = algo.evolve_population(pop).clone(data)
        max_fitness = pop.schedules[0].calculate_fitness()
        chart_data.append((idx + 1, pop.average_fitness(), max_fitness))

        idx += 1
        if max_fitness >= 1.0:
            break


    return pop

import time

start_time = time.time()

final_pop = perform(initial_pop)

end_time = time.time()

st.subheader(f"Total Waktu: {end_time - start_time} detik")
st.subheader(f"Total Iterasi: {chart_data[-1][0]} iterasi")

st.line_chart(pd.DataFrame(chart_data, columns=["iteration", "avg_fitness", "max_fitness"]), x="iteration", y=["avg_fitness", "max_fitness"])


def render_pop(pop: Population, streamlit_target=st):
    schedule_pairs = zip(
        streamlit_target.tabs([f"Schedule #{idx}" for idx, _ in enumerate(pop.schedules)]),
        pop.schedules
    )
    schedule_data: Schedule
    for schedule_tab, schedule_data in schedule_pairs:
        schedule_tab.subheader(f"Max Fitness: {schedule_data.calculate_fitness()}")
        schedule_tab.table([x.__dict__ for x in schedule_data.academic_classes])
        pass


col1, col2 = st.columns(2)

render_pop(initial_pop, col1)
render_pop(final_pop, col2)
