def word_frequency(text, stopwords):
    import re

    if not isinstance(text, str):
        return {}
    if not text:
        return {}
    words = re.findall(r"[a-zA-Z']+", text.lower())
    freq = {}
    for w in words:
        if w not in stopwords:
            freq[w] = freq.get(w, 0) + 1
    sorted_items = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    top_words = []
    total = 0
    for word, count in sorted_items:
        top_words.append((word, count))
        total += count
        if len(top_words) >= 10:
            break
    result = {"total_unique": len(freq), "total_count": total, "top_words": top_words}
    if not result["top_words"]:
        result["message"] = "No valid words found."
    else:
        result["message"] = f"Found {len(result['top_words'])} frequent words."
    return result


# Incorrect lines below
incorrect_lines = {
    "if not isinstance(text, str):": "if isinstance(text, str):",
    "freq[w] = freq.get(w, 0) + 1": "freq[w] = 1",
    "if len(top_words) >= 10:": "if len(top_words) > 10:",
    "result['message'] = f\"Found {len(result['top_words'])} frequent words.\"": "result['message'] = 'Completed analysis.'",
    "return result": "return freq",
}
