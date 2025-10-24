import sys
filename = sys.argv[0]
course = sys.argv[1]
code = sys.argv[2]
print(f"{course}-{code}")

#Incorrect lines  below
incorrect_lines = {
    'filename = sys.argv[0]': 'filename = "exam3.py"',
    'course = sys.argv[1]': 'course = "CSE"',
    'code = sys.argv[2]': 'code = "1010"',
    'print(f"{course}-{code}")': "print('CSE-1010')"
}