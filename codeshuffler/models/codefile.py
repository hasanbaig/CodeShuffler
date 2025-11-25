import os

from codeshuffler.lib.generator import read_original_code


class CodeFile:
    def __init__(self, path: str):
        self.path = path
        self.filename = os.path.basename(path)
        self.correct_sol = None
        self.wrong_inst = None
        self.wrong_inst_dict = None
        self.warning_msg = None
        self.loaded = False

    def load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            (
                self.correct_sol,
                self.wrong_inst,
                self.wrong_inst_dict,
                self.warning_msg,
            ) = read_original_code(f)
        self.loaded = True
