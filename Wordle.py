#Built uopn aAa1928's wordle clone

import sys
import time
import random

from DataProcessing import DataProcessing
from Solver import Solver

data = DataProcessing()
solve = Solver()

answers, guesses = data.get_data()

heuristic_list = data.get_heuristic_list(guesses=guesses, func=data.default_heuristic)
penalize_heuristic_list = data.get_heuristic_list(guesses=guesses, func=data.penalize_heuristic)

# Code to go through every entry

file = open('output.txt', 'w')

start_time = time.time()
for answer in answers:
    copy = penalize_heuristic_list[:]
    temp = solve.greedy(copy, answer.lower(), "salet")
    file.write(str(temp))
    if len(temp) > 6:
        file.write(" FAIL")
    file.write("\n")
file.close()

end_time = time.time()

elapsed_time = end_time - start_time

print("Elapsed time:", elapsed_time, "seconds")

#print(solve.greedy(penalize_heuristic_list, "whelp", "salet"))
