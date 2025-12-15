def find_even(nums):
    for n in nums:
        if n % 2 == 0:
            return n
    return None


# Incorrect lines below
incorrect_lines = {"for n in nums:": "for i in range(len(nums)):", "return None": "return i"}
