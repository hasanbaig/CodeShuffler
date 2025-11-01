# -------------------------------------------------------------------------------
# CodeShuffler © 2023 by Hasan Baig is licensed under CC BY-NC-SA 4.0. To view
# a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
# -------------------------------------------------------------------------------

import ast
import random
import sys

from . import settings
from .utils import sequence_similarity


def read_original_code(read_code):
    original_code = read_code.readlines()
    code_wo_empty_lines = [line for line in original_code if line.strip() != ""]
    correct_sol = [line.rstrip("\n") for line in code_wo_empty_lines]

    incorrect_sol = []
    incorrect_sol_dict = {}

    for idx, line in enumerate(correct_sol):
        if "incorrect_lines" in line.lower():
            # Include preceding comment if exists
            if idx > 0 and correct_sol[idx - 1].strip().startswith("#"):
                idx -= 1
            dict_lines = correct_sol[idx:]
            correct_sol = correct_sol[:idx]
            dict_str = "\n".join(dict_lines)
            dict_part = dict_str.split("=", 1)[1].strip()
            incorrect_sol_dict = ast.literal_eval(dict_part)
            incorrect_sol = list(incorrect_sol_dict.values())
            # todo: add functionality checking if dict length is longer than available items to swap
            break
    return correct_sol, incorrect_sol, incorrect_sol_dict


def gen_correct_answer(correct_sol, shuffled_sol):
    correct_answer = ""
    all_lines = [str(i + 1) for i in range(len(shuffled_sol))]
    remain_lines = all_lines.copy()
    used_shuffled_line_indices = set()

    for line_cor in correct_sol:
        for i, line_shuf in enumerate(shuffled_sol):
            shuffled_line_number = i + 1
            # Check if this line number (index) has already been used
            if i in used_shuffled_line_indices:
                continue
            shuffled_line = line_shuf[line_shuf.index(")") + 2 :]

            if line_cor == shuffled_line:
                correct_answer += str(shuffled_line_number) + ","
                used_shuffled_line_indices.add(i)  # Mark this line number as used
                break  # Move to the next line in correct_sol
    correct_answer = correct_answer[:-1]
    # generating remaining lines which are not present the correct answer
    # Use the set of all lines to efficiently calculate remaining lines
    used_line_numbers = set(correct_answer.split(","))
    remain_lines = [line for line in all_lines if line not in used_line_numbers]

    return correct_answer, remain_lines


def shuffle_rand_choices(answers_array):
    # shuffling the random choices
    random.shuffle(answers_array)
    return answers_array


def incorrect_instructions(input_code, wrong_inst):
    code_w_incorrect_instrctns = input_code + wrong_inst
    return code_w_incorrect_instrctns


def gen_random_choices(correct_answer, no_of_choices):
    random_choices = []
    choice_array = correct_answer.split(",")
    while len(random_choices) < no_of_choices - 1:
        choice = random.sample(choice_array, k=len(choice_array))
        choice = ",".join(choice)
        if choice != correct_answer:
            random_choices.append(choice)

    random_choices.append(correct_answer)
    random_choices = shuffle_rand_choices(random_choices)
    return random_choices


def gen_random_choices_wICinst(correct_answer, no_of_choices, remain_lines):
    random_choices = []
    choice_array = correct_answer.split(",")
    while len(random_choices) < no_of_choices - 1:
        if settings.first_same_X_lines_MCQ >= len(choice_array):
            print(
                "Error: first_same_X_lines_MCQ is greater than or equal to total lines available. Please restrict to few lines."
            )
            sys.exit(1)
        first_X_lines_MCQ = correct_answer.split(",")[: settings.first_same_X_lines_MCQ]
        remaining_array = correct_answer.split(",")[len(first_X_lines_MCQ) :]
        k = random.randint(len(remaining_array) - 1, len(remaining_array) + len(remain_lines) - 1)
        # added to ensure we dont sample more than available
        k = min(k, len(remaining_array + remain_lines))
        remaining_choices = random.sample(remaining_array + remain_lines, max(k, 0))
        choices = first_X_lines_MCQ + remaining_choices
        random.shuffle(choices[3:])
        choice = ",".join(map(str, choices))
        similarity = sequence_similarity(choice.split(","), correct_answer.split(","))
        if choice != correct_answer and similarity >= len(correct_answer.split(",")) - 2:
            if choice not in random_choices:
                random_choices.append(choice)
    random_choices.append(correct_answer)
    random_choices = shuffle_rand_choices(random_choices)
    return random_choices


def generate_partials(num_swaps_limit, numbered_code, incorrect_lines, answer_mcq):
    copied_code = numbered_code.copy()
    correct_answer_mcq = [int(x) for x in answer_mcq.split(",")]
    partial_answer_bank = []
    for line in numbered_code:
        if num_swaps_limit <= 0:
            break
        code = line.split(")", 1)[1].strip()  # extract code without line number
        if code in incorrect_lines:
            # print(f"Found line to swap: '{code}'")
            index_to_swap = numbered_code.index(line)  # get the index of the line to swap
            line_to_swap_with = incorrect_lines[code]  # get the incorrect line to swap with
            # print(f"Line to swap with: '{line_to_swap_with}'")
            if any(
                line_to_swap_with in line for line in copied_code
            ):  # ensure the line to swap with exists in the copied code
                # print(f"Swapping line '{code}' with '{line_to_swap_with}'")
                index_of_line_to_swap_with = next(
                    i
                    for i, line in enumerate(copied_code)
                    if line_to_swap_with in line  # find index of line to swap with
                )
                to_swap_index = correct_answer_mcq.index(index_to_swap + 1)
                correct_answer_mcq[to_swap_index] = (
                    index_of_line_to_swap_with + 1
                )  # update answer key by swapping with incorrect line
                partial_answer_bank.append(",".join(map(str, correct_answer_mcq)))
                num_swaps_limit -= 1
    return partial_answer_bank
