# -------------------------------------------------------------------------------
# CodeShuffler © 2023 by Hasan Baig is licensed under CC BY-NC-SA 4.0. To view 
# a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
# ------------------------------------------------------------------------------- 

from . import settings
import random
from PIL import Image, ImageDraw, ImageFont
import ast
import hashlib

def similarity_preserving_shuffle(lines): #a deterministic shuffle in order to preserve code similarity
    def line_hash(line):
        return int(hashlib.md5(line.encode()).hexdigest(), 16)
    salt = 12345  #fixed for deterministic behavior
    def salted_hash(line):
        return (line_hash(line) ^ salt)
    return sorted(lines, key=salted_hash)

def read_original_code(read_code):
    original_code = read_code.readlines()
    code_wo_empty_lines = [line for line in original_code if line.strip() != ""]
    correct_sol = [line.rstrip("\n") for line in code_wo_empty_lines]

    incorrect_sol = []
    incorrect_sol_dict = {}

    for idx, line in enumerate(correct_sol):
        if "incorrect_lines" in line:
            # Include preceding comment if exists
            if idx > 0 and correct_sol[idx-1].strip().startswith("#"):
                idx -= 1
            dict_lines = correct_sol[idx:]
            correct_sol = correct_sol[:idx]
            dict_str = "\n".join(dict_lines)
            dict_part = dict_str.split("=", 1)[1].strip()
            incorrect_sol_dict = ast.literal_eval(dict_part)
            incorrect_sol = list(incorrect_sol_dict.values())
            break

    return correct_sol, incorrect_sol, incorrect_sol_dict

def shuffle_sol(correct_sol):
    random_code = similarity_preserving_shuffle(correct_sol.copy())
    
    #removing the indents for programming blocks
    for el in range(len(random_code)):
        random_code[el] = f"({el+1}) " + random_code[el]#.strip()        #Remove strip() function to include tabs
        
    return random_code

def gen_correct_answer(correct_sol, shuffled_sol):
    correct_answer = ""
    all_lines = [ str(i+1) for i in range(len(shuffled_sol))]
    remain_lines = all_lines.copy()
    used_shuffled_line_indices = set() 
    
    for line_cor in correct_sol:
        found = False
        for i, line_shuf in enumerate(shuffled_sol):
            shuffled_line_number = i + 1
            
            # Check if this line number (index) has already been used
            if i in used_shuffled_line_indices:
                continue
                
            shuffled_line = line_shuf[line_shuf.index(")") + 2:] 
            
            if line_cor == shuffled_line:
                correct_answer += str(shuffled_line_number) + ","
                used_shuffled_line_indices.add(i) # Mark this line number as used
                break # Move to the next line in correct_sol

    correct_answer = correct_answer[:-1]
    
    # generating remaining lines which are not present the correct answer 
    # Use the set of all lines to efficiently calculate remaining lines
    used_line_numbers = set(correct_answer.split(","))
    remain_lines = [line for line in all_lines if line not in used_line_numbers]
            
    return correct_answer, remain_lines

def convert_to_image(shuffled_sol, file_name):
    image = Image.new('RGB', (settings.image_x_dim, settings.image_y_dim), color = (255, 255, 255))   
    d= ImageDraw.Draw(image)
    fnt = ImageFont.truetype('lib/Source_Code_Pro/static/SourceCodePro-Medium.ttf', 15)
    
    y = 0
    for line in shuffled_sol:
        d.text((10,y), line.strip(), font = fnt, fill = (0, 0, 0))
        y += 20
    
    file_path = f"shuffledcodeimages/{file_name}.png"
    image.save(file_path)    
 
#shuffeling the random choices
def shuffle_rand_choices(answers_array):
    random.shuffle(answers_array)
    return answers_array
                
def gen_random_choices(correct_answer, no_of_choices):
    random_choices = []
    
    # choice_array = list(correct_answer)
    choice_array = correct_answer.split(",")
    while len(random_choices) < no_of_choices-1:
        choice = random.sample(choice_array, k=len(choice_array))
        choice = ",".join(choice)
        if choice != correct_answer:
            random_choices.append(choice)
        
    random_choices.append(correct_answer)        
    random_choices = shuffle_rand_choices(random_choices)
    return random_choices        

# Function to calculate similarity between two sequences
def sequence_similarity(seq1, seq2):
    set1 = set(seq1)
    set2 = set(seq2)
    return len(set1.intersection(set2))

def gen_random_choices_wICinst(correct_answer, no_of_choices, remain_lines):
    random_choices = []
    choice_array = correct_answer.split(",")
    total_lines = len(choice_array + remain_lines)

    while len(random_choices) < no_of_choices - 1:
        first_X_lines_MCQ = correct_answer.split(",")[:settings.first_same_X_lines_MCQ]
        remaining_array = correct_answer.split(",")[len(first_X_lines_MCQ):]
        k = random.randint(len(remaining_array) - 1, len(remaining_array) + len(remain_lines) - 1)
        #added to ensure we dont sample more than available
        k = min(k, len(remaining_array + remain_lines))
        remaining_choices = random.sample(remaining_array + remain_lines, max(k,0))
        choices = first_X_lines_MCQ + remaining_choices
        random.shuffle(choices[3:])
        choice = ",".join(map(str, choices))
        similarity = sequence_similarity(choice.split(","), correct_answer.split(","))
        if choice != correct_answer and similarity >= len(correct_answer.split(",")) - 1:
            random_choices.append(choice)
    
    random_choices.append(correct_answer)
    random_choices = shuffle_rand_choices(random_choices)
    return random_choices        

def incorrect_instructions(input_code, wrong_inst):
    code_w_incorrect_instrctns = input_code + wrong_inst
    # print_code(code_w_incorrect_instrctns, "##### Code with Incorrect Instructions #####")
    return code_w_incorrect_instrctns

def numerize_code(input_code):
    #Convert a list of code lines into a dictionary with line numbers as keys
    num_line_pair = {}
    for line in range(len(input_code)):
        num_line_pair[line+1] = input_code[line]
    return num_line_pair

def swap_lines(num_swaps_limit, numbered_code, incorrect_lines):
    #given a dictionary of incorrect options and dictionary of the base code, swap corresponding lines within the numbered code
    code_copy = numbered_code.copy()
    num_swaps = 0
    for num, _ in code_copy.items():
        if num_swaps >= num_swaps_limit:
            break
        if num in incorrect_lines:
            code_copy[num] = incorrect_lines[num]
            print(f"Swapped line {code_copy[num]} with {incorrect_lines[num]}")
            num_swaps += 1
    swapped_code = list(code_copy.values())
    return swapped_code

def generate_partial_answers(base_code, no_of_choices, incorrect_lines):
    num_partials = no_of_choices//2
    partial_options_code = []
    numerized_code = numerize_code(base_code)
    for swap in range(1, 0, -1):
        partial_option = swap_lines(swap, numerized_code, incorrect_lines)
        partial_options_code.append(partial_option)
    return partial_options_code

def gen_partial_credit_answer(partial_code_snippet, shuffled_exam_question):
    partial_answer, _ = gen_correct_answer(partial_code_snippet, shuffled_exam_question)
    return partial_answer
    

def print_code(in_code, message = "##### Code #####"):
    print()
    print(message)
    for line in in_code:
        print(line)