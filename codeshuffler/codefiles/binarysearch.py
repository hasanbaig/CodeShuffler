def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


# Incorrect lines below
incorrect_lines = {
    "while left <= right:": "while left < right:",
    "elif nums[mid] < target:": "if nums[mid] > target:",
    "return -1": "return None",
}
