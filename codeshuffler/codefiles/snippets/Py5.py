file = open("data.txt", "r+")
data = file.readlines()
sum = 0
for value in data:
    sum += int(value)
avg = sum / len(data)
file.write(str(avg))
file.close()

# Incorrect lines  below
incorrect_lines = {
    "avg = sum/len(data)": "avg = sum/data",
    "file.write(str(avg))": "file.write(avg)",
    "sum += int(value)": "sum += value",
}
