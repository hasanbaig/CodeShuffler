def max_num(nums):
    max_val = nums[0]
    for n in nums:
        if n > max_val:
            max_val = n
    return max_val

#Incorrect lines below
incorrect_lines = {
    "max_val = nums[0]": "max_val = 0",
    "return max_val": "return n"
}
