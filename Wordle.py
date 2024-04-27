#Built uopn aAa1928's wordle clone

import sys
import time
import random
import multiprocessing
import os

from DataProcessing import DataProcessing
from Solver import Solver

def run(file_, seed_, func):
    data = DataProcessing()
    solve = Solver()

    directory_name = "run_all"
    os.makedirs(directory_name, exist_ok=True)

    answers, guesses = data.get_data()

    default_heuristic_list = data.get_heuristic_list(guesses=guesses, func=data.default_heuristic)                  # 1. no weighting just letter distribution from Oxford Dictionary 1995                   
    wordle_default_heuristic_list = data.get_heuristic_list(guesses=guesses, func=data.wordle_heuristic)            # 2. clone of default_heuristic just uses letter distribution generated from wordle
    penalize_heuristic_list = data.get_heuristic_list(guesses=guesses, func=data.penalize_heuristic)                # 3. weighting just letter distribution from Oxford Dictionary 1995
    wordle_penalize_heuristic_list = data.get_heuristic_list(guesses=guesses, func=data.wordle_penalize_heuristic)  # 4. clone of penalize_heuristic just uses letter distribution generated from wordle

    output = file_ + ".txt"
    output_file = os.path.join(directory_name, output)
    list_as_string = seed_
    wordle_seed = list_as_string.split()
    func_to_use = int(func)

    if(func_to_use == 1):
        heuristic = default_heuristic_list
    elif(func_to_use == 2):
        heuristic = wordle_default_heuristic_list
    elif(func_to_use == 3):
        heuristic = penalize_heuristic_list
    elif(func_to_use == 4):
        heuristic = wordle_penalize_heuristic_list

    # Code to go through every entry

    file = open(output_file, 'w')
    count = 0.0

    graph = [0,0,0,0,0,0,0,0]

    start_time = time.perf_counter()
    for answer in answers:
        copy = heuristic[:]
        temp = solve.greedy(copy, answer.lower(), wordle_seed)
        count += len(temp) 
        file.write(str(temp))
        if len(temp) <= 6:
            graph[len(temp)] += 1
        elif len(temp) > 6:
            graph[-1] += 1
            file.write(" FAIL ")
            file.write(str(len(temp)))
        elif temp[-1] != answer.lower():
            graph[-1] += 1
            file.write(" WAS NOT SOLVED")
        file.write("\n")

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time

    file.write("\n")
    for i in range(1, len(graph)):
        if i <=6:
            file.write(f'{i}    | ({graph[i]})\n')
        else:
            file.write(f'FAIL | ({graph[i]})\n')
    file.write("\n")    

    file.write("Total Guesses: ")
    file.write(str(count))
    file.write("\n")

    file.write("Mean: ")
    file.write(str(count / 2309))
    file.write("\n")

    file.write("Elapsed time: ")
    file.write(str(elapsed_time))
    file.write(" seconds\n")

    file.close()

args_list = [
    ("salet_default", "salet", "1"),
    ("salet_wordle_default", "salet", "2"),
    ("salet_penalize", "salet", "3"),
    ("salet_wordle_penalize", "salet", "4"),
    ("soare_default", "soare", "1"),
    ("soare_wordle_default", "soare", "2"),
    ("soare_penalize", "soare", "3"),
    ("soare_wordle_penalize", "soare", "4"),
    ("three_best_default", "raise clout nymph", "1"),
    ("three_best_wordle_default", "raise clout nymph", "2"),
    ("three_best_penalize", "raise clout nymph", "3"),
    ("three_best_wordle_penalize", "raise clout nymph", "4"),
    ("adieu_default", "adieu", "1"),
    ("adieu_wordle_default", "adieu", "2"),
    ("adieu_penalize", "adieu", "3"),
    ("adieu_wordle_penalize", "adieu", "4")
]

processes = []

total_start = time.perf_counter()

for file_name, seed_word, mode in args_list:
    p = multiprocessing.Process(target=run, args=[file_name, seed_word, mode])
    p.start()
    processes.append(p)

for process in processes:
    process.join()

total_end = time.perf_counter()

print(f'Finished in {round(total_end-total_start, 2)} seconds')

# print(solve.greedy(heuristic, "eater", wordle_seed))
