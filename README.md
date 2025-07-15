CodeShuffler empowers instructors to rearrange lines within coding files, regardless of the programming language used, producing an output image that presents the shuffled lines of code. Additionally, it generates multiple-choice options, with one of them signifying the correct sequence of coding lines. This tool simplifies the process of conducting paper-based coding assessments, eliminating the need for manual grading and streamlining the evaluation process for educators.

CodeShuffler, along with all associated coding files, and the assessment template, are copyrighted by Hasan Baig and are made publicly available under the following license terms: 

"CodeShuffler © 2023 by Hasan Baig is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)". 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
 

### Instructions
1. You need to install Python Pillow library, which you can do simply by executing the following command:
`pip install pillow`

2. To run the program, you need to execute `main.py` file alongwith the input code filename as a commandline argument. 
For example, to shuffle the code, for example `samplecode.py`, first place it in the directory `\codefiles\` and then execute the following:
`python main.py samplecode.py`

### Settings

1. You can optionally add incorrect instructions at the end of the input code after adding the comment line "**#Incorrect lines below**". See `samplecode.py` for help. Then set the switch `include_incorrect_instructions = True` in `lib\settings.py` file. 

2. You can optionally specify to keep **X** number of lines same in the generated multiple choice questions by setting the value of switch `first_same_X_lines_MCQ` in `lib\settings.py` file. 

3. You can specify how many multiple choice options you want to generate by setting the value of a switch `no_of_choices` in `lib\settings.py` file. 
