from config import config
from data_utils import get_data
from population import Population
from perform import perform
from genetic_algo import GeneticAlgoV1, GeneticAlgoV2
import pickle
import os
import time
import sys
import signal

if __name__ == '__main__':
    start_time = time.time()
    end_time = time.time()


    def write_log(text: str) -> None:
        with open(log_path, 'a') as log_file:
            log_file.write(text)
            log_file.write("\n")
        pass


    def prog_end():
        global end_time
        end_time = time.time()
        finish_msg = "Program terminated, elapsed time: {0} seconds".format(end_time - start_time)
        write_log(finish_msg)
        print(finish_msg)


    def sigterm_handler(signal, frame):
        prog_end()
        sys.exit(0)
        pass


    signal.signal(signal.SIGTERM, sigterm_handler)

    saved_pop_path = config['schedule_dump_bin_path']
    log_path = config['schedule_dump_log_path']

    data = get_data()

    algo = GeneticAlgoV2(
        population_size=config['population_size'],
        elite_schedules_count=config['number_of_elites'],
        tournament_size=config['tournament_size'],
        mutation_rate=config['mutation_rate'],
        crossover_rate=config['crossover_rate'],
        data=data
    )

    initial_pop = None

    init_msg = "POP SIZE = {0}\nELITE SIZE = {1}\nTOURNAMENT SIZE {2}\nMUTATION RATE = {3}\nCROSSOVER RATE={4}".format(
        algo.population_size,
        algo.elite_schedules_count,
        algo.tournament_size,
        algo.mutation_rate,
        algo.crossover_rate
    )

    write_log(init_msg)
    print(init_msg)

    if os.path.exists(saved_pop_path):
        print("Loading " + saved_pop_path)
        # Open the file for reading in binary mode
        with open(saved_pop_path, "rb") as file:
            # Load the object from the file
            initial_pop = pickle.load(file)
    else:
        print("Starting from new pop")
        initial_pop = Population(config['population_size'], data)


    def start_callback(pop: Population, i: int, max_fitness: float):
        pop.best_schedule().dump_csv('output/initial_best_schedule.csv')
        pass

    def iteration_callback(pop: Population, i: int, max_fitness: float):
        log_text = "ITERATION: {0}; Fitness: {1:.20f}".format(i, max_fitness)

        write_log(log_text)
        print(log_text)
        pass


    def finish_callback(
            pop: Population,
            i: int,
            max_fitness: float,
            solution_found_at_iteration: int,
            solution_found_at_time: float
    ):
        log_text = "FINISH: {0}; Fitness: {1:.20f}".format(i, max_fitness)

        if solution_found_at_iteration != -1:
            solution_text = "SOLUSI DITEMUKAN PADA ITERASI KE: {} ({}) Detik".format(solution_found_at_iteration, solution_found_at_time)
            write_log(solution_text)
            print(solution_text)
        else:
            solution_text = "SOLUSI TIDAK DITEMUKAN"
            write_log(solution_text)
            print(solution_text)


        write_log(log_text)
        print(log_text)

        # Open a file for writing in binary mode
        with open(saved_pop_path, "wb") as file:
            pickle.dump(pop, file)

        pop.best_schedule().dump_csv('output/final_best_schedule.csv')

        prog_end()

        pass


    start_time = time.time()

    final_pop = perform(
        data=data,
        algo=algo,
        pop=initial_pop,
        max_iter=config['max_iterations'],
        start_callback=start_callback,
        iter_callback=iteration_callback,
        finish_callback=finish_callback
    )
