import pickle

from data_utils import to_json
from population import Population
from config import config


with open(config['schedule_dump_bin_path'], "rb") as file:
    initial_pop: Population = pickle.load(file)


best_schedule = initial_pop.best_schedule()

import numpy as np

# if academic_class.room.seating_capacity < academic_class.course.max_students:
#     total_conflicts += 1
#
# if academic_class.department.is_laboratory and academic_class.room.seating_capacity < 30:
#     total_conflicts += 1
#
# if academic_class.meeting_time.credits < academic_class.department.credits:
#     total_conflicts += 1



print(
    to_json([{
        'seating_capacity': ac.room.seating_capacity,
        'max_students': ac.room.seating_capacity,

    } for ac in best_schedule.academic_classes])
)