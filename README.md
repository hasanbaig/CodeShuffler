
<img width="1347" height="268" alt="codeshuffler-name" src="https://github.com/user-attachments/assets/72b7871f-83ef-4783-9f5a-9ed64b44f666" />
<br />
<br />

[![Main Release](https://github.com/ShawnSpitzel/CodeShuffler-v2/actions/workflows/release.yml/badge.svg)](https://github.com/ShawnSpitzel/CodeShuffler-v2/actions/workflows/release.yml)
[![Main Release](https://github.com/ShawnSpitzel/CodeShuffler-v2/actions/workflows/ci.yml/badge.svg)](https://github.com/ShawnSpitzel/CodeShuffler-v2/actions/workflows/ci.yml)
[![Windows ](https://img.shields.io/badge/Download-Windows-blue?logo=windows)](
https://github.com/ShawnSpitzel/CodeShuffler-v2/releases/tag/v1.0.0
)


CodeShuffler empowers instructors to rearrange lines within coding files, regardless of the programming language used, producing an output image that presents the shuffled lines of code. Additionally, it generates multiple-choice options, with one of them signifying the correct sequence of coding lines. This tool simplifies the process of conducting paper-based coding assessments, eliminating the need for manual grading and streamlining the evaluation process for educators.

CodeShuffler, along with all associated coding files, and the assessment template, are copyrighted by Hasan Baig and are made publicly available under the following license terms: 
 

## Installation

### Option 1: Download Executable

1. Go to the **Releases** tab or press the **Download** button above
2. Download the executable for your operating system
3. Launch the application

**Supported platforms**
- Windows (released)
- macOS (release, buggy)
- Linux (coming v1.1.0)

### Option 2: Clone Repo

```bash
git clone https://github.com/<your-username>/CodeShuffler.git
cd CodeShuffler
python -m venv venv
source venv/bin/activate  # If on Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Instructions

**CodeShuffler** provides two primary workflows:

- **CodeShuffler**: Generates shuffled code-based questions by pairing correct code with structured incorrect variants.
- **ExamShuffler**: Shuffles full exams (questions and/or answers) while preserving correctness and formatting.

### CodeShuffler Instructions

**CodeShuffler** expects two sections in the source file:

1. Correct code snippet
2. Incorrect variants dictionary, explicitly marked

The correct implementation must appear first, followed by a dictionary incorrect_lines in format {correct:incorrect}. 
An example is provided below:

```python
def max_num(nums):
    max_val = nums[0]
    for n in nums:
        if n > max_val:
            max_val = n
    return max_val
# Incorrect lines below
incorrect_lines = {
    "max_val = nums[0]": "max_val = 0",
    "return max_val": "return n"
}
```
Note that the incorrect lines delimiter and incorrect_lines variable name must be copied verbatim. More snippets are also available
at codeshuffler/codefiles/snippets.

### ExamShuffler Instructions

**ExamShuffler** expects a .docx Word file structured in a standard exam format.

Questions may be numbered or bulleted, each question must contain exactly one set of answer choices, and 
formatting should remain consistent across the document. If you'd like to keep track of the correct answer for a given question,
denote a * character at the end of the option. Additionally, if using code snippets within your question, denote
the code block with ```<code>...<code/>``` tags. An example is provided below.

```text
1. What is the output of the following code?

<code>
print(2 + 3 * 4)
</code>

A) 20  
B) 14*  
C) 24  
D) 10  
```

When finished, you will have the option to view your shuffled exam with an answer key, without the answer key, or with both. In later versions,
users will also have the ability to change their header & footer templates through the Settings menu. As of right now, the default template is the standard
University of Connecticut exam template.

"CodeShuffler ©2026 by Hasan Baig is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)". 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


