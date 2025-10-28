from partialcredit import sort_by_similarity


def test_basic_case():
    options = [
        "3,1,4,8,6,9,7,10",
        "3,1,4,8,10,2,9,5",
        "3,1,4,8,10,9,2",
        "3,1,4,8,9,2,10",
        "3,1,4,8,9,7,10",
    ]
    correct = "3,1,4,8,9,2,10"
    sorted_opts = sort_by_similarity(options, correct)
    assert sorted_opts[0] == "3,1,4,8,9,2,10"
    assert sorted_opts[1] == "3,1,4,8,9,7,10"
    print(sorted_opts)
    print("test_basic_case passed")


def test_perfect_match_only():
    options = ["1,2,3,4"]
    correct = "1,2,3,4"
    sorted_opts = sort_by_similarity(options, correct)
    assert sorted_opts == ["1,2,3,4"]
    print("test_perfect_match_only passed")


def test_no_common_elements():
    options = ["9,8,7", "a,b,c", "x,y,z"]
    correct = "1,2,3"
    sorted_opts = sort_by_similarity(options, correct)
    assert set(sorted_opts) == set(options)
    print("test_no_common_elements passed")


def test_partial_overlap():
    options = ["1,2,3,4,5", "1,2,3,9,9", "1,2,4,4,4"]
    correct = "1,2,3,4,5"
    sorted_opts = sort_by_similarity(options, correct)
    assert sorted_opts[0] == "1,2,3,4,5"
    assert sorted_opts[1] == "1,2,3,9,9"
    print("test_partial_overlap passed")


def test_different_lengths():
    options = ["1,2,3", "1,2", "1,2,3,4,5"]
    correct = "1,2,3,4,5"
    sorted_opts = sort_by_similarity(options, correct)
    assert sorted_opts[0] == "1,2,3,4,5"
    assert sorted_opts[1] == "1,2,3"
    print("test_different_lengths passed")


if __name__ == "__main__":
    test_basic_case()
    test_perfect_match_only()
    test_no_common_elements()
    test_partial_overlap()
    test_different_lengths()
    print("All tests passed!")
