from typing import Callable, Optional

from genetic_algo import GeneticAlgo
from data_utils import Data
from population import Population


def perform(
        data: Data,
        algo: GeneticAlgo,
        pop: Population,
        max_iter=Optional[int],
        iter_callback: Optional[Callable[[Population, int, float], None]] = None,
        finish_callback: Optional[Callable[[Population, int, float], None]] = None
):
    iteration_counter = 0

    pop = pop.clone(data)

    max_fitness = pop.schedules[0].calculate_fitness()

    try:
        while True:
            iteration_counter = iteration_counter + 1
            pop = algo.evolve_population(pop).clone(data)
            max_fitness = pop.schedules[0].calculate_fitness()

            if iter_callback is not None:
                iter_callback(pop, iteration_counter, max_fitness)

            if max_fitness >= 1.0:
                break

            if (max_iter is not None) and (iteration_counter > max_iter):
                break
        pass
    except KeyboardInterrupt:
        if finish_callback is not None:
            finish_callback(pop, iteration_counter, max_fitness)
        return pop
        pass

    if finish_callback is not None:
        finish_callback(pop, iteration_counter, max_fitness)

    return pop
