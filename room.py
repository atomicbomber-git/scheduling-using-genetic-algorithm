class Room:
    def __init__(self, name, seating_capacity: int):
        self.name = name
        self.seating_capacity = seating_capacity

    def __str__(self):
        return f"{self.name} ({self.seating_capacity})"
