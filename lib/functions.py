# -------------------------------------------------------------------------------
# CodeShuffler © 2023 by Hasan Baig is licensed under CC BY-NC-SA 4.0. To view 
# a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
# ------------------------------------------------------------------------------- 

from . import settings
import random
from PIL import Image, ImageDraw, ImageFont
import ast
import hashlib

def similarity_preserving_shuffle(lines):
    def line_hash(line):
        # Convert line to a hash integer
        return int(hashlib.md5(line.encode()).hexdigest(), 16)
    
    # Sort by hash, but we can mix in a secret salt for “randomness”
    salt = 12345  # optional, fixed for deterministic behavior
    def salted_hash(line):
        return (line_hash(line) ^ salt)
    
    # Sort lines by their salted hash
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
    
    for line_cor in correct_sol:
        for line_shuf in shuffled_sol:
            # print(f"Instruction: {line_shuf}  , index of ): ", line_shuf.index(")"))
            shuffled_line = line_shuf[line_shuf.index(")") + 2:] 
            # if line_cor == line_shuf[4:]:
            if line_cor == shuffled_line:
                correct_answer += str(shuffled_sol.index(line_shuf)+1) + ","
            
    correct_answer = correct_answer[:-1]
    
    
    #generating remaining lines which are not present the correct answer 
    for line in all_lines:
        if line in correct_answer:
            remain_lines.remove(line)
            
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
        # Select the first three lines from the correct answer
        first_X_lines_MCQ = correct_answer.split(",")[:settings.first_same_X_lines_MCQ]
        remaining_array = correct_answer.split(",")[len(first_X_lines_MCQ):]
        
        # Define the size of the remaining part of the random sequence (k)
        # k = random.randint(len(choice_array) - 1, len(choice_array) + len(remain_lines) - 1)
        k = random.randint(len(remaining_array) - 1, len(remaining_array) + len(remain_lines) - 1)
        
        # Randomly select numbers from choice_array and remain_lines to complete the sequence
        # remaining_choices = random.sample(choice_array + remain_lines, k - 3)
        remaining_choices = random.sample(remaining_array + remain_lines, k)
        
        # Combine the first three lines and the remaining choices
        choices = first_X_lines_MCQ + remaining_choices
        
        # Shuffle the remaining choices to randomize the order
        random.shuffle(choices[3:])
        
        # Convert the choices to a string
        choice = ",".join(map(str, choices))

        # Calculate similarity between the random sequence and the correct answer
        similarity = sequence_similarity(choice.split(","), correct_answer.split(","))

        # Check if the generated sequence is close to the correct answer
        if choice != correct_answer and similarity >= len(correct_answer.split(",")) - 1:
            random_choices.append(choice)
    
    random_choices.append(correct_answer)
    random_choices = shuffle_rand_choices(random_choices)
    return random_choices        

def incorrect_instructions(input_code, wrong_inst):
    code_w_incorrect_instrctns = input_code + wrong_inst
    print_code(code_w_incorrect_instrctns, "##### Code with Incorrect Instructions #####")
    return code_w_incorrect_instrctns

def numerize_code(input_code):
    num_line_pair = {}
    for line in range(len(input_code)):
        num_line_pair[line+1] = input_code[line]
    return num_line_pair

def swap_lines(num_partials, numbered_code, incorrect_lines):
    code_copy = numbered_code.copy()
    num_swaps = num_partials
    for num, _ in code_copy.items():
        if num_swaps == 0:
            break
        if num in incorrect_lines:
            code_copy[num] = incorrect_lines[num]
            num_swaps -= 1
    swapped_code = list(code_copy.values())
    return swapped_code

def generate_partial_options(base_code, no_of_choices, incorrect_lines, remain_lines):
    num_partials = no_of_choices//2
    partial_options = []
    numerized_code = numerize_code(base_code)
    for swap in range(num_partials, 0, -1):
        partial_option = swap_lines(swap, numerized_code, incorrect_lines)
        lettered_partial_option = gen_correct_answer(partial_option, shuffle_sol(partial_option))[0]
        random_partial_option = gen_random_choices_wICinst(lettered_partial_option, 1, remain_lines)[0]
        partial_options.append(random_partial_option)
    print("Generated Partial Options: ", partial_options)
    return partial_options

def generate_partial_answers(base_code, no_of_choices, incorrect_lines):
    num_partials = no_of_choices//2
    partial_options = []
    numerized_code = numerize_code(base_code)
    for swap in range(num_partials, 0, -1):
        partial_option = swap_lines(swap, numerized_code, incorrect_lines)
        partial_options.append(partial_option)
    return partial_options
    

def print_code(in_code, message = "##### Code #####"):
    print()
    print(message)
    for line in in_code:
        print(line)