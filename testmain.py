# -------------------------------------------------------------------------------
# CodeShuffler © 2023 by Hasan Baig is licensed under CC BY-NC-SA 4.0. To view 
# a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
# ------------------------------------------------------------------------------- 

from lib import settings
from lib import functions
import sys

#Reading code, extracting lines separately
if sys.argv[1]:
    file_name = sys.argv[1]
else:
    print("Enter the code's filename you want to shuffle.")
    sys.exit(1)
    
read_code = open('codefiles/'+file_name)
correct_sol, wrong_inst, wrong_inst_dict = functions.read_original_code(read_code)

# message = "##### Correct Solution #####"
# functions.print_code(correct_sol, message)
correct_sol_w_incorrect= functions.incorrect_instructions(correct_sol, wrong_inst)
# shuffled_sol = functions.shuffle_sol(correct_sol)
# message = "##### Shuffled Question #####"
# functions.print_code(shuffled_sol, message)
# correct_answer, remain_lines = functions.gen_correct_answer(correct_sol, shuffled_sol)

# random_choices = functions.gen_random_choices_wICinst(correct_answer, settings.no_of_choices, remain_lines)
# partial_options = functions.generate_partial_options(correct_sol, settings.no_of_choices, wrong_inst_dict, remain_lines)

#Shuffling Test
shuffled_correct = functions.shuffle_sol(correct_sol_w_incorrect)
correct_answer, remain_lines = functions.gen_correct_answer(correct_sol, shuffled_correct)
random_choices = functions.gen_random_choices_wICinst(correct_answer, settings.no_of_choices, remain_lines)
functions.print_code(shuffled_correct, "##### Shuffled Exam Question #####")
partial_options = functions.generate_partial_answers(correct_sol_w_incorrect, settings.no_of_choices, wrong_inst_dict)
partial_answers = []
for option in partial_options:
    shuffled_option = functions.shuffle_sol(option)
    answer, _ = functions.gen_correct_answer(option, shuffled_option)
    partial_answers.append(answer)
    functions.print_code(shuffled_option, "##### Shuffled Partial Option #####")
print()
print("Correct answer: ", correct_answer)
print("Multiple answers: ", random_choices) 
print("Partial credit options: ", partial_answers)
print()    


