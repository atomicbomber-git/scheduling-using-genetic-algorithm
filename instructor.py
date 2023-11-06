class Instructor:
    def __init__(self, instructor_id, name):
        self.id = instructor_id
        self.name = name

    def __str__(self):
        return f"[{self.id}] {self.name}"
