def similarity(a, b):
    a_parts = a.split(',')
    b_parts = b.split(',')
    matches = 0
    for i in range(min(len(a_parts), len(b_parts))):
        if a_parts[i] == b_parts[i]:
            matches += 1
    return matches / max(len(a_parts), len(b_parts))
def find_closest(options, correct_answer):
    best = None
    best_score = -1
    for choice in options:
        score = similarity(choice, correct_answer)
        if score > best_score:
            best_score = score
            best = choice
    return best
def sort_by_similarity(options, correct_answer):
    options_copy = options.copy()
    sorted_options = []
    i = 0
    while i < len(options):
        closest = find_closest(options_copy, correct_answer)
        sorted_options.append(closest)
        options_copy.remove(closest)
        i += 1
    return sorted_options