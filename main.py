# -------------------------------------------------------------------------------
# CodeShuffler © 2023 by Hasan Baig is licensed under CC BY-NC-SA 4.0. To view 
# a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
# ------------------------------------------------------------------------------- 

from lib import functions

#Reading code, extracting lines separately
file_name = 'samplecode.py'
read_code = open('codefiles/'+file_name)
correct_sol = functions.read_original_code(read_code)


print("##### Correct Solution #####")
for line in range(len(correct_sol)):
    print(correct_sol[line])
print()

#Shuffle the original code lines and tag them with line numbers
shuffled_sol = functions.shuffle_sol(correct_sol)
print("***** Shuffled Solution *****")
for line in range(len(shuffled_sol)):
    print(shuffled_sol[line])
print()

#generating the correct answer with the correct order of code lines
correct_answer = functions.gen_correct_answer(correct_sol, shuffled_sol)

#generating multiple random choices including the correct answer
no_of_choices = 4
random_choices = functions.gen_random_choices(correct_answer, no_of_choices)

print()
print("Multiple answers: ", random_choices) 
print("Correct answer: ", correct_answer)    

#generating shuffled code image
print("******* Generating Shuffled code image ......")
functions.convert_to_image(shuffled_sol, file_name)
print("******* Output image stored in the shuffledcodeimage directory!")
