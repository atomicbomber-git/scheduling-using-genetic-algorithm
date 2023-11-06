class Course:
    def __init__(self, name, instructors, max_students):
        self.max_students = max_students
        self.instructors = instructors
        self.name = name

    def __str__(self):
        return f"{self.name} ({self.max_students})"
