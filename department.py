from typing import List, Optional


class Department:
    def __init__(
            self,
            name: str,
            credit_amount: int = 2,
            department_courses: Optional[List] = None,
            is_laboratory: bool = False
    ):
        self.name = name
        self.credits = credit_amount
        self.is_laboratory = is_laboratory

        if department_courses is None:
            self.courses = []
        else:
            self.courses = department_courses

    def __str__(self):
        return f"{self.name} ({self.credits} SKS){' (Lab)' if self.is_laboratory else ''}"
