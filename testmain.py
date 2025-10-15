# -------------------------------------------------------------------------------
# CodeShuffler © 2023 by Hasan Baig is licensed under CC BY-NC-SA 4.0. To view 
# a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
# ------------------------------------------------------------------------------- 

from lib import settings
from lib import functions
import sys
if sys.argv[1]:
    file_name = sys.argv[1]
else:
    print("Enter the code's filename you want to shuffle.")
    sys.exit(1)
    
read_code = open('codefiles/'+file_name)
correct_sol, wrong_inst, wrong_inst_dict = functions.read_original_code(read_code)

correct_sol_w_incorrect = functions.incorrect_instructions(correct_sol, wrong_inst)

shuffled_correct = functions.shuffle_sol(correct_sol_w_incorrect)
functions.print_code(shuffled_correct, "##### Shuffled Exam Question #####")

correct_answer, remain_lines = functions.gen_correct_answer(correct_sol, shuffled_correct)

random_choices = functions.gen_random_choices_wICinst(correct_answer, settings.no_of_choices, remain_lines)
partial_options_code = functions.generate_partial_answers(correct_sol_w_incorrect, settings.no_of_choices, wrong_inst_dict)

partial_answers = []
for option_code_snippet in partial_options_code:
    functions.print_code(option_code_snippet, "##### Partial Option Code Snippet (Correct Order) #####")
    partial_answer = functions.gen_partial_credit_answer(option_code_snippet, shuffled_correct)
    partial_answers.append(partial_answer)
    
print()
print("Correct answer: ", correct_answer)
print("Multiple answers: ", random_choices) 
print("Partial credit options: ", partial_answers)
print()