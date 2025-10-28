def area(r):
    pi = 3.14
    Area = pi * r**2
    return Area


A = area(4)

# Incorrect lines
incorrect_lines = {"def area (r):": "def area(2):", "Area = pi * r**2": "Area = pi * r * 2"}
