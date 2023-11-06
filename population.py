from schedule import Schedule
from data import Data

class Population:
    def __init__(self, pop_size, data):
        schedule_id_counter = 0
        self.schedules = []

        for _ in range(0, pop_size):
            self.schedules.append(Schedule(schedule_id_counter, data))
            schedule_id_counter += 1
            pass

        self.sort_schedules_by_fitness()

    def clone(self, data):
        pop = Population(0, data)
        for self_schedule in self.schedules:
            pop.schedules.append(self_schedule)
        return pop

    def sort_schedules(self):
        for iter_schedule in self.schedules:
            iter_schedule.academic_classes.sort(
                key=lambda ac: ac.meeting_time.start_time
            )
        return self

    def schedule_desc(self):
        return ", ".join([str(x.id) for x in self.schedules])

    def sort_schedules_by_fitness(self):
        self.schedules.sort(key=lambda x: x.calculate_fitness(), reverse=True)

    def average_fitness(self):
        return sum([schedule.calculate_fitness() for schedule in self.schedules]) / len(self.schedules)
