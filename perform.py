from typing import Callable, Optional

from genetic_algo import GeneticAlgoV1, GeneticAlgoV2
from data_utils import Data
from population import Population


def perform(
        data: Data,
        algo: GeneticAlgoV1|GeneticAlgoV2,
        pop: Population,
        max_iter=Optional[int],
        start_callback: Optional[Callable[[Population, int, float], None]] = None,
        iter_callback: Optional[Callable[[Population, int, float], None]] = None,
        finish_callback: Optional[Callable[[Population, int, float, int], None]] = None
):
    iteration_counter = 0

    pop = pop.clone(data)
    max_fitness = pop.schedules[0].fitness

    if start_callback is not None:
        start_callback(pop, iteration_counter, max_fitness)

    solution_found_at = -1

    try:
        while True:
            if (max_iter is not None) and (iteration_counter >= max_iter):
                break

            iteration_counter = iteration_counter + 1
            pop = algo.evolve_population(pop).clone(data)

            max_fitness = pop.schedules[0].fitness

            if (max_fitness >= 1.0) and (solution_found_at == -1):
                solution_found_at = iteration_counter

            if iter_callback is not None:
                iter_callback(pop, iteration_counter, max_fitness)
        pass
    except KeyboardInterrupt:
        if finish_callback is not None:
            finish_callback(pop, iteration_counter, max_fitness, solution_found_at)
        return pop
        pass

    if finish_callback is not None:
        finish_callback(pop, iteration_counter, max_fitness, solution_found_at)

    return pop
