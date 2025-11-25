def merge_sorted(l1, l2):
    i = j = 0
    result = []
    while i < len(l1) and j < len(l2):
        if l1[i] < l2[j]:
            result.append(l1[i])
            i += 1
        else:
            result.append(l2[j])
            j += 1
    while i < len(l1):
        result.append(l1[i])
        i += 1
    while j < len(l2):
        result.append(l2[j])
        j += 1
    return result


# Incorrect lines below
incorrect_lines = {
    "if l1[i] < l2[j]:": "if l1[i] > l2[j]:",
    "while i < len(l1):": "for i in range(len(l1)):",
    "return result": "return []",
}
