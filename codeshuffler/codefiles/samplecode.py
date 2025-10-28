students = {}
students["Saleh"] = ["CSE-1010", "CSE-2050"]
print(students)
print(students["Saleh"][1])

# Incorrect lines below
incorrect_lines = {
    'students["Saleh"] = ["CSE-1010", "CSE-2050"]': 'students[Saleh] = ["CSE-1010", "CSE-2050"]',
    "print(students)": "print(Saleh)",
    'print(students["Saleh"][1])': 'print(students["Saleh"])',
}
