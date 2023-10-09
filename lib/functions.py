import random
from PIL import Image, ImageDraw, ImageFont

def read_original_code(read_code):
    correct_sol = read_code.readlines()
    #Removing \n character from each line
    for el in range(len(correct_sol)):
        correct_sol[el] = correct_sol[el].split('\n')[0]
    
    return correct_sol    

def shuffle_sol(correct_sol):
    random_code = random.sample(correct_sol, k=len(correct_sol))
    
    #removing the indents for programming blocks
    for el in range(len(random_code)):
        random_code[el] = f"({el+1}) " + random_code[el]#.strip()        #Remove strip() function to include tabs
        
    return random_code

def gen_correct_answer(correct_sol, shuffled_sol):
    correct_answer = ""
    for line_cor in correct_sol:
        for line_shuf in shuffled_sol:
            # print(f"Instruction: {line_shuf}  , index of ): ", line_shuf.index(")"))
            shuffled_line = line_shuf[line_shuf.index(")") + 2:] 
            # if line_cor == line_shuf[4:]:
            if line_cor == shuffled_line:
                correct_answer += str(shuffled_sol.index(line_shuf)+1) + ","
    correct_answer = correct_answer[:-1]
    return correct_answer

def convert_to_image(shuffled_sol, file_name):
    image = Image.new('RGB', (500, 300), color = (255, 255, 255))   
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