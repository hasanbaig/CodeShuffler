import copy
import random
import re

from docx import Document
from docx2python import docx2python
from docx.shared import Pt


def create_exam_docx(exam_dict, output_path):
    doc = Document()
    doc.add_paragraph("")  # blank line

    for qnum, content in exam_dict.items():
        q_para = doc.add_paragraph()
        q_run = q_para.add_run(f"{qnum}) {content['question']}")
        q_run.font.size = Pt(11)
        q_para.paragraph_format.space_after = Pt(6)

        for i, choice in enumerate(content["choices"]):
            letter = chr(97 + i)  # a,b,c,d
            c_para = doc.add_paragraph(f"{letter}) {choice}")
            c_para.paragraph_format.left_indent = Pt(18)
            c_para.paragraph_format.space_after = Pt(3)

        doc.add_paragraph("")

    doc.save(output_path)
    print(f"Exam rebuilt and saved to {output_path}")


def parse_exam(doc_path: str):
    with docx2python(doc_path) as docx_content:
        text = docx_content.text

    lines = []
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped:  # skip empty lines
            lines.append(stripped)

    exam = {}
    current_qnum = None
    question_text = []
    choices: list[str] = []

    # regex patterns
    question_pattern = re.compile(r"^(\d+)[).]")
    choice_pattern = re.compile(r"^\(?[a-dA-D]\)?[).]")

    for line in lines:
        if question_pattern.match(line):
            if current_qnum is not None:
                exam[current_qnum] = {
                    "question": " ".join(question_text).strip(),
                    "choices": choices,
                }
            match = question_pattern.match(line)
            if match:
                current_qnum = int(match.group(1))
            question_text = [re.sub(question_pattern, "", line).strip()]
            choices = []

        elif choice_pattern.match(line) and current_qnum is not None:
            choice_text = re.sub(choice_pattern, "", line).strip()
            choices.append(choice_text)

        elif current_qnum is not None:
            question_text.append(line)
    if current_qnum is not None:
        exam[current_qnum] = {"question": " ".join(question_text).strip(), "choices": choices}
    return exam


def shuffle_questions(exam_dict):
    exam_copy = copy.deepcopy(exam_dict)
    question_items = list(exam_copy.items())
    random.shuffle(question_items)

    shuffled_exam = {}
    for new_qnum, (_, content) in enumerate(question_items, start=1):
        shuffled_exam[new_qnum] = content

    return shuffled_exam


def shuffle_answers(exam_dict):
    exam_copy = copy.deepcopy(exam_dict)
    for _, content in exam_copy.items():
        if "choices" in content and isinstance(content["choices"], list):
            random.shuffle(content["choices"])
    return exam_copy


def print_exam_dict(exam_dict):
    print("\n" + "=" * 80)
    print(f"EXAM CONTENTS - {len(exam_dict)} Questions")
    print("=" * 80 + "\n")

    for question_num in sorted(exam_dict.keys()):
        question_data = exam_dict[question_num]
        print(f"Question {question_num}:")
        print(f"  {question_data['question']}")
        print()
        labels = ["a", "b", "c", "d", "e", "f"]
        print("  Choices:")
        for idx, choice in enumerate(question_data["choices"]):
            if idx < len(labels):
                print(f"    ({labels[idx]}) {choice}")
            else:
                print(f"    - {choice}")
        print("\n" + "-" * 80 + "\n")
