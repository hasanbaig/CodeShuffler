import os
import sys

from codeshuffler.lib.parser import (
    create_exam_docx,
    parse_exam,
    print_exam_dict,
    shuffle_answers,
    shuffle_questions,
)

if sys.platform == "darwin":  # macOS
    os.environ["QT_MAC_WANTS_LAYER"] = "1"

exam_dict = parse_exam("codeshuffler/codefiles/Sample_Exam.docx")

print_exam_dict(exam_dict)
shuffled_exam = shuffle_answers(exam_dict)
shuffled_exam = shuffle_questions(shuffled_exam)
create_exam_docx(shuffled_exam, "codeshuffler/codefiles/Rebuilt_Exam.docx")

# app = QApplication(sys.argv)

# app.setApplicationName("CodeShuffler")
# app.setOrganizationName("CodeShuffler")
# app.setApplicationDisplayName("CodeShuffler")

# gui = CodeShufflerGUI()
# gui.show()
# sys.exit(app.exec_())
