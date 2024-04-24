#Built uopn aAa1928's wordle clone
import time
from DataProcessing import DataProcessing
from numba import njit

data = DataProcessing()

# DEBUG = False

# def timing(*args):
#     def _timing(f):
#         if debug:
#             @wraps(f)
#             def wrap(*args, **kw):
#                 ts = time.perf_counter()
#                 result = f(*args, **kw)
#                 te = time.perf_counter()
#                 print(f"{f.__name__} took {te-ts:2.4f} sec")
#                 return result
#             return wrap
#         else:
#             return f
#     if len(args) == 1 and callable(args[0]):
#         # No optional argument to decorator
#         debug = True
#         return _timing(args[0])
#     else:
#         # Optional argument to decorator
#         debug = args[0]
#         return _timing

# function to solve wordles goes in here
# idea is that they take in the heuristic list and then make predictions based on that and list of letter positions


class Solver:

    def check_word(self, hidden, guess):
        mask = []
        for i in range(0, 5):
            if (hidden[i] == guess[i]):
                mask.append(2)
            elif (guess[i] in hidden):
                mask.append(1)
            else:
                mask.append(0)

        return mask
    
    def remove_green_from_yellow(self, main_list, reference_list):
        return [tpl for tpl in main_list if tpl[0] not in [item[0] for item in reference_list]]

    # check_word for automatic solving
    # green is a list of tuples that maps a char to the correct position
    # yellow is a list of tuples that maps char to positions it can't be in
    # gray is a list of chars that aren't in the hidden word 
    def check_word_auto(self, hidden, guess, green, yellow, gray):
        for i in range(0, 5):
            if (hidden[i] == guess[i]):
                #if all(guess[i] not in tpl for tpl in green):
                    green.append((guess[i], i))
            elif (guess[i] in hidden):
                yellow.append((guess[i], i))
                self.remove_green_from_yellow(yellow, green)
            else:
                if all(guess[i] not in char for char in gray):
                    gray.append(guess[i])

        return green, yellow, gray
    
    # helper function that checks pos of letter
    def char_in_positions(self, string, positions):
        found = 0
        if len(positions) == 0:
            return True
        for pos in positions:
            if pos[0] == string[pos[1]]:
                found += 1
        return found == len(positions)

    def char_wihin(self, string, positions):
        chars = [tpl[0] for tpl in positions]
        not_used = [tpl[1] for tpl in positions]
        found = 0
        if not chars:
            return True  
        return all(char in string for char in chars)

    # greedy algo that picks the best word from the heuristic list that meets the criteria
    def greedy(self, heuristic_list, hidden, guess):
        sol_list = []
        green, yellow, gray = self.check_word_auto(hidden, guess, [], [], [])
        sol_list.append(guess)

        while hidden not in sol_list:  
            if not heuristic_list:  
                break
            
            best = max(heuristic_list, key=lambda x: x[0])

            if not any(char in gray for char in best[1]):                
                if not self.char_in_positions(best[1], yellow) and self.char_wihin(best[1], yellow):
                    if self.char_in_positions(best[1], green):
                        sol_list.append(best[1])
                        green, yellow, gray = self.check_word_auto(hidden, best[1], green, yellow, gray)
                elif not yellow:
                    sol_list.append(best[1])
                    green, yellow, gray = self.check_word_auto(hidden, best[1], green, yellow, gray)

            heuristic_list.remove(best) 

            if best[1] == hidden:  
                break

        return sol_list
    
        #     sol_list = []
        # green, yellow, gray = self.check_word_auto(hidden, guess, [], [], [])
        # sol_list.append(guess)

        # while hidden not in sol_list:
        #     if not heuristic_list:  
        #         break
        
        #     best = max(heuristic_list, key=lambda x: x[0])

        #     if not any(char in gray for char in best[1]):
        #         if not (self.char_in_positions(best[1], yellow)):
        #             if not yellow:
        #                 sol_list.append(best[1])
        #                 green, yellow, gray = self.check_word_auto(hidden, best[1], green, yellow, gray)
        #             if(self.char_in_positions(best[1], green)):
        #                 sol_list.append(best[1])
        #                 green, yellow, gray = self.check_word_auto(hidden, best[1], green, yellow, gray)

        #     heuristic_list.remove(best) 

        # return sol_list 

