from typing import List

import pandas as pd

import timeslot
from course import Course
from data import Data
from department import Department
from instructor import Instructor
from room import Room
import datetime
import json

DEPT_FIELD = "Department Name"

source_departments = [
    Department("PEMROGRAMAN BERBASIS KERANGKA KERJA", 3, ["course6", "course8"], is_laboratory=True),
    Department("JARINGAN KOMPUTER", 3, ["course10", "course16", "course22"], is_laboratory=True),
    Department("ALGORITMA GENETIKA", 3, ["course1"]),
    Department("SISTEM TEMU KEMBALI INFORMASI", 3, ["course1"]),
    Department("LOGIKA SAMAR", 3, ["course1"]),
    Department("KEAMANAN KOMPUTER", 3, ["course7", "course5", "course9"]),
    Department("METODE NUMERIK", 3, ["course23", "course14", "course20"]),
    Department("ARSITEKTUR DAN ORGANISASI KOMPUTER", 3, ["course28", "course36", "course43"]),
    Department("KECERDASAN BERKOLONI", 3, ["course2"]),
    Department("KECERDASAN BUATAN", 3, ["course11", "course17", "course24"]),
    Department("LOGIKA INFORMATIKA", 3, ["course29", "course40", "course49"]),
    Department("DESAIN PENGALAMAN PENGGUNA", 3, ["course12", "course18", "course25"], is_laboratory=True),
    Department("ALGORITMA DAN STRUKTUR DATA", 3, ["course30", "course37", "course44"], is_laboratory=True),
    Department("SISTEM PENDUKUNG KEPUTUSAN", 3, ["course3"]),
    Department("PENJAMINAN KUALITAS PERANGKAT LUNAK", 3, ["course3"]),
    Department("TEORI BAHASA DAN OTOMATA", 3, ["course31", "course38", "course45"]),
    Department("PEMROGRAMAN BERORIENTASI OBJEK", 3, ["course13", "course19", "course26"], is_laboratory=True),
    Department("PEMROGRAMAN WEB LANJUT", 3, ["course13", "course19", "course26"], is_laboratory=True),
    Department("ALJABAR LINEAR", 3, ["course32", "course39", "course46"]),
    Department("AIK 2 (IBADAH MUAMALAH DAN AKHLAK)", 3, ["course47", "course41", "course34"]),
    Department("PENDIDIKAN KEWARGANEGARAAN", 3, ["course4", "course33", "course48"]),
    Department("AIK 4 (ISLAM & ILMU PENGETAHUAN)", 3, ["course27", "course21", "course15"]),
    Department("ENGLISH FOR SPECIFIC PURPOSES", 3, ["course35", "course42", "course50"]),
]

raw_departments = pd.DataFrame(source_departments, columns=[DEPT_FIELD])
ROOM_CODE_FIELD = "Kode Ruangan"
STUDENT_CAPACITY_FIELD = "Kapasitas"
raw_rooms = pd.DataFrame([
    ("R1", 20),
    ("R2", 20),
    ("R3", 20),
    ("R4", 30),
    ("R5", 30)
], columns=[ROOM_CODE_FIELD, STUDENT_CAPACITY_FIELD])
ID_FIELD = "ID"
TIMESLOT_FIELD = "Pertemuan"
raw_meeting_times = pd.DataFrame([(idx, ts) for idx, ts in enumerate(timeslot.timeslots)], columns=[
    ID_FIELD,
    TIMESLOT_FIELD
])
INSTRUCTOR_NAMES_FIELD = "Nama Instruktur"
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


COURSE_ID_FIELD = "CourseID"
STUDENT_AMOUNT_FIELD = "Jumlah Siswa"

INSTRUCTOR_KEY_FIELD = "Nama Instruktur FIELD"
COURSE_NAMES_FIELD = "Course IDS"

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


def find_course_by_name(course_name, courses: List[Course]):
    for course in courses:
        if course.name == course_name:
            return course
    return None


def get_data() -> Data:
    instructors_list = raw_instructors.apply(lambda row: Instructor(row[ID_FIELD], row[INSTRUCTOR_NAMES_FIELD]),
                                             axis=1).to_list()
    plain_courses = (raw_courses.apply(lambda row: raw_course_to_course(row, instructors_list), axis=1)).to_list()

    converted_depts = [
        Department(
            orig_dept.name,
            orig_dept.credits,
            [find_course_by_name(course, plain_courses) for course in orig_dept.courses],
            orig_dept.is_laboratory
        ) for orig_dept in
        source_departments
    ]

    return Data(
        departments=converted_depts,
        instructors=instructors_list,
        courses=plain_courses,
        rooms=(raw_rooms.apply(lambda row: Room(row[ROOM_CODE_FIELD], row[STUDENT_CAPACITY_FIELD]), axis=1)).to_list(),
        meeting_times=(raw_meeting_times.apply(lambda row: row[TIMESLOT_FIELD], axis=1)).to_list()
    )


def serializer(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%A %H:%M")
    return obj.__dict__


def to_json(obj):
    json.dumps(obj, default=serializer, sort_keys=True, indent=4)


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