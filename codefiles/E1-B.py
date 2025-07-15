studied = int(input())
if studied > 6:
    print("I am a warrior!")
elif 4 <= studied <= 6:
    print("I could do better")
elif studied < 4:
    print("I should take 1010 seriously.")
else:
    print("Wrong input")

#Incorrect lines
studied = input()
if studied <= 4:
