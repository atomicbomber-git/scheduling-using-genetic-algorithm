import random
from typing import List

from population import Population
from schedule import Schedule


class GeneticAlgo:
    def __init__(
            self,
            population_size: int,
            elite_schedules_count: int,
            tournament_size: int,
            mutation_rate: float,
            crossover_rate: float,
            data
    ):
        self.population_size = population_size
        self.elite_schedules_count = elite_schedules_count
        self.tournament_size = tournament_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.data = data
        pass

    def mutate_schedule(self, sche: Schedule) -> Schedule:
        new_schedule = Schedule(sche.id, self.data, None, fitness=0)

        for idx, academic_class in enumerate(sche.academic_classes):
            if self.mutation_rate <= random.random():
                new_schedule.academic_classes[idx] = academic_class

        new_schedule.calculate_and_cache_fitness()

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
        return max(tournament_participants, key=lambda schedule: schedule.fitness).clone()

    def crossover_population(self, pop: Population):
        crossover_pop = Population(0, self.data)

        pop.sort_schedules_by_fitness()
        for idx in range(0, self.elite_schedules_count):
            crossover_pop.schedules.append(pop.schedules[idx])
            pass

        for _ in range(self.elite_schedules_count, self.population_size):
            parent_schedule_1 = self.select_tournament_schedule(pop)
            parent_schedule_2 = self.select_tournament_schedule(pop)

            child_schedule = self.get_schedule_by_crossover(parent_schedule_1, parent_schedule_2)

            crossover_pop.schedules.append(child_schedule)

        return crossover_pop

    def get_schedule_by_crossover(self, parent_schedule_1, parent_schedule_2):
        for idx, _ in enumerate(parent_schedule_1.academic_classes):
            if random.random() > self.crossover_rate:
                parent_schedule_1.academic_classes[idx] = parent_schedule_2.academic_classes[idx].clone()

        parent_schedule_1.calculate_and_cache_fitness()
        return parent_schedule_1

    def evolve_population(self, pop: Population) -> Population:
        population = self.mutate_population(self.crossover_population(pop))

        population.sort_schedules_by_fitness()
        return population

    pass
