def area (r):
    pi = 3.14
    A = pi * r**2
    return A
A = area(2)

#Incorrect lines
incorrect_lines = {
    "def area (r):": "def area(2):",
    "A = pi * r**2": "A = pi * r * 2"
}