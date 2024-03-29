from schedule import Schedule


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

    def best_schedule(self) -> Schedule:
        return max(self.schedules, key=lambda schedule: schedule.fitness)

    def sort_schedules(self):
        def custom_sort_key(dt):
            day_of_week_index = dt.weekday()
            time_str = dt.strftime('%H:%M')
            return day_of_week_index, time_str

        for iter_schedule in self.schedules:
            iter_schedule.academic_classes.sort(
                key=lambda ac: custom_sort_key(ac.meeting_time.start_time)
            )
        return self

    def schedule_desc(self):
        return ", ".join([str(x.id) for x in self.schedules])

    def sort_schedules_by_fitness(self):
        self.schedules.sort(key=lambda x: x.fitness, reverse=True)

    def average_fitness(self):
        return sum([schedule.calculate_fitness() for schedule in self.schedules]) / len(self.schedules)