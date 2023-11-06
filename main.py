import streamlit as st
import pandas as pd
from data_utils import get_data
from genetic_algo import GeneticAlgo
from perform import perform
from population import Population
from schedule import Schedule
import pickle

data = get_data()

st.set_page_config(layout="wide")
st.title("Penjadwalan dengan Genetic Algorithm")
st.divider()
st.subheader("Pengaturan Data")

POPULATION_SIZE = st.number_input("POPULATION_SIZE", value=9)
NUMB_OF_ELITE_SCHEDULES = st.number_input("NUMB_OF_ELITE_SCHEDULES", value=1)
TOURNAMENT_SELECTION_SIZE = st.number_input("TOURNAMENT_SELECTION_SIZE", value=3, min_value=0,
                                            max_value=POPULATION_SIZE)
MUTATION_RATE = st.number_input("MUTATION_RATE", value=0.5, min_value=0.0, max_value=1.0, step=0.1)

saved_pop_path = "output/schedule.pkl"

with open(saved_pop_path, "rb") as file:
    # Load the object from the file
    initial_pop = pickle.load(file)

algo = GeneticAlgo(
    population_size=POPULATION_SIZE,
    elite_schedules_count=NUMB_OF_ELITE_SCHEDULES,
    tournament_size=TOURNAMENT_SELECTION_SIZE,
    mutation_rate=MUTATION_RATE,
    data=data
)

chart_data = []

import time

start_time = time.time()


def append_chart_data(pop: Population, i: int, max_fitness: float):
    global chart_data
    chart_data.append((i + 1, pop.average_fitness(), max_fitness))


final_pop = perform(
    data=data,
    algo=algo,
    pop=initial_pop,
    max_iter=10,
    iter_callback=append_chart_data
)

end_time = time.time()

st.subheader(f"Total Waktu: {end_time - start_time} detik")
st.subheader(f"Total Iterasi: {chart_data[-1][0]} iterasi")

st.line_chart(pd.DataFrame(chart_data, columns=["iteration", "avg_fitness", "max_fitness"]), x="iteration",
              y=["avg_fitness", "max_fitness"])


def render_pop(pop: Population, streamlit_target=st):
    schedule_pairs = zip(
        streamlit_target.tabs([f"Schedule #{idx}" for idx, _ in enumerate(pop.schedules)]),
        pop.schedules
    )
    schedule_data: Schedule
    for schedule_tab, schedule_data in schedule_pairs:
        schedule_tab.subheader(f"Max Fitness: {schedule_data.calculate_fitness()}")
        schedule_tab.table([x.__dict__ for x in schedule_data.academic_classes])
        pass


col1, col2 = st.columns(2)

render_pop(initial_pop.sort_schedules(), col1)
render_pop(final_pop.sort_schedules(), col2)
