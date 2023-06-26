from lib import functions

#Reading code, extracting lines separately
read_code = open('codefiles/final-1-files.py')
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


