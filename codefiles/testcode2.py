def two_sum(nums, target):
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return (num_map[complement], i)
        num_map[num] = i
    return None

#Incorrect lines below
incorrect_lines = {
    3: "for i in range(len(nums)):", 
    8: "return num_map"
}            