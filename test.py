from typing import List
import random
import pickle
from config import config
from population import Population

with open(config['schedule_dump_bin_path'], "rb") as file:
    pop: Population = pickle.load(file)
    pop.schedules[0].dump_csv('output/schedule.csv')

