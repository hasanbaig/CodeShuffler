# -------------------------------------------------------------------------------
# CodeShuffler © 2023 by Hasan Baig is licensed under CC BY-NC-SA 4.0. To view
# a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
# -------------------------------------------------------------------------------

import sys

from codeshuffler.lib import settings
from codeshuffler.lib.generator import (
    gen_correct_answer,
    gen_random_choices_wICinst,
    generate_partials,
    incorrect_instructions,
    read_original_code,
)
from codeshuffler.lib.utils import convert_to_image, print_code, shuffle_sol

# Reading code, extracting lines separately
if sys.argv[1]:
    file_name = sys.argv[1]
else:
    print("Enter the code's filename you want to shuffle.")
    sys.exit(1)

read_code = open("codefiles/" + file_name)

# Extract correct and incorrect lines from the code file
correct_sol, wrong_inst, wrong_inst_dict = read_original_code(read_code)
correct_sol_w_incorrect = incorrect_instructions(correct_sol, wrong_inst)

# Display shuffled question
shuffled_question = shuffle_sol(correct_sol_w_incorrect)
print_code(shuffled_question, "##### Shuffled Exam Question #####")

# Generating correct answer, partial credit options, and random choices
correct_answer, remain_lines = gen_correct_answer(correct_sol, shuffled_question)
partial_option = generate_partials(
    len(wrong_inst_dict), shuffled_question, wrong_inst_dict, correct_answer
)
random_choices = gen_random_choices_wICinst(correct_answer, settings.no_of_choices, remain_lines)
# Generating shuffled code image without indentation
image_shuffled_sol = []

for el in range(len(shuffled_question)):
    line = shuffled_question[el].split(")", 1)
    image_shuffled_sol.append(line[0] + ") " + line[-1].strip())
print("******* Generating Shuffled code image ......")
convert_to_image(image_shuffled_sol, file_name)
print(f"Image generated and stored in ~/images/ directory as {file_name}.png")
print()
print("Correct answer: ", correct_answer)
print("Multiple answers: ", random_choices)
print("Partial credit options: ", partial_option)
print()
