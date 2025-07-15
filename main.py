from lib import settings, functions
import sys

#Reading code, extracting lines separately
if sys.argv[1]:
    file_name = sys.argv[1]
else:
    print("Enter the code's filename you want to shuffle.")
    sys.exit(1)
    
read_code = open('codefiles/'+file_name)
correct_sol, wrong_inst = functions.read_original_code(read_code)


message = "##### Correct Solution #####"
functions.print_code(correct_sol, message)


if settings.include_incorrect_instructions:
    with_incorrect_insts = functions.incorrect_instructions(correct_sol, wrong_inst)
    shuffled_sol = functions.shuffle_sol(with_incorrect_insts)
else:    
    #Shuffle the original code lines and tag them with line numbers
    shuffled_sol = functions.shuffle_sol(correct_sol)

message = "***** Shuffled Solution *****"
functions.print_code(shuffled_sol, message)

#generating the correct answer with the correct order of code lines
correct_answer, remain_lines = functions.gen_correct_answer(correct_sol, shuffled_sol)


if settings.include_incorrect_instructions:
    random_choices = functions.gen_random_choices_wICinst(correct_answer, settings.no_of_choices, remain_lines)
else:
    random_choices = functions.gen_random_choices(correct_answer, settings.no_of_choices)

print()
print("Multiple answers: ", random_choices) 
print("Correct answer: ", correct_answer)
print()    

######## Shuffled Code for Image without indendation
image_shuffled_sol = []
for el in range(len(shuffled_sol)):
    line = shuffled_sol[el].split(")", 1)
    image_shuffled_sol.append(line[0] + ") " + line[-1].strip())
    # print(test_shuffled_sol[el])
    

#generating shuffled code image
print("******* Generating Shuffled code image ......")
functions.convert_to_image(image_shuffled_sol, file_name)
print(f"Image generated and stored in ~/shuffledcodeimages/ directory as {file_name}.png")
