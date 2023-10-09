from lib import functions
import sys
#Reading code, extracting lines separately
if sys.argv[1]:
    file_name = sys.argv[1]
else:
    print("Enter the code's filename you want to shuffle.")
    sys.exit(1)
    
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
print(f"Correct Answer: {correct_answer}")


#generating multiple random choices including the correct answer
no_of_choices = 4
random_choices = functions.gen_random_choices(correct_answer, no_of_choices)

print()
print("Multiple answers: ", random_choices) 
print("Correct answer: ", correct_answer)    

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
