from typing import List
import random


x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
y = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]


def one_point_crossover(list_a: List, list_b: List):
    point = random.randint(0, len(list_a))
    return list_a[:point] + list_b[point:]




print(one_point_crossover(x, y))