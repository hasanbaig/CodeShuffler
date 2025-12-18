
<img width="1347" height="268" alt="codeshuffler-name" src="https://github.com/user-attachments/assets/72b7871f-83ef-4783-9f5a-9ed64b44f666" />
<br />
<br />


CodeShuffler empowers instructors to rearrange lines within coding files, regardless of the programming language used, producing an output image that presents the shuffled lines of code. Additionally, it generates multiple-choice options, with one of them signifying the correct sequence of coding lines. This tool simplifies the process of conducting paper-based coding assessments, eliminating the need for manual grading and streamlining the evaluation process for educators.

CodeShuffler, along with all associated coding files, and the assessment template, are copyrighted by Hasan Baig and are made publicly available under the following license terms: 

"CodeShuffler © 2023 by Hasan Baig is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)". 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
 

### Instructions
1. To run the program, execute the following code snippets:
`python -m venv .venv`
`source .venv/bin/activate  # Windows: .\.venv\Scripts\activate`
`pip install -r requirements.txt`
`python main.py`

### Settings

2. You can optionally add incorrect instructions at the end of the input code after adding the comment line "**#Incorrect lines below**". See `samplecode.py` for help. Then set the switch `include_incorrect_instructions = True` in `lib\settings.py` file. 

3. You can optionally specify to keep **X** number of lines same in the generated multiple choice questions by setting the value of switch `first_same_X_lines_MCQ` in `lib\settings.py` file. 

4. You can specify how many multiple choice options you want to generate by setting the value of a switch `no_of_choices` in `lib\settings.py` file. 
# CodeShuffler-v2

