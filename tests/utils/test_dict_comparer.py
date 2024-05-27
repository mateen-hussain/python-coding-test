from src.utils.dict_comparer import dict_differences


def test_dict_differences_missing():
    dict1 = {"a": 1, "b": 2}
    dict2 = {"a": 1, "b": 2, "c": 3}
    expected_output = {
        "missing": {"c": 3},
        "new_data": {},
        "different": {},
    }
    assert dict_differences(dict1, dict2) == expected_output


def test_dict_differences_new_data():
    dict1 = {"a": 1, "b": 2, "c": 3}
    dict2 = {"a": 1, "b": 2}
    expected_output = {
        "missing": {},
        "new_data": {"c": 3},
        "different": {},
    }
    assert dict_differences(dict1, dict2) == expected_output


def test_dict_differences_different():
    dict1 = {"a": 1, "b": 2, "c": 3}
    dict2 = {"a": 1, "b": 2, "c": 4}
    expected_output = {
        "missing": {},
        "new_data": {},
        "different": {"c": (3, 4)},
    }
    assert dict_differences(dict1, dict2) == expected_output


def test_dict_differences_no_changes():
    dict1 = {"a": 1, "b": 2, "c": 3}
    dict2 = {"a": 1, "b": 2, "c": 3}
    expected_output = {
        "missing": {},
        "new_data": {},
        "different": {},
    }
    assert dict_differences(dict1, dict2) == expected_output


def test_dict_differences_all_cases():
    dict1 = {"a": 1, "b": 2, "c": 3}
    dict2 = {"b": 2, "c": 4, "d": 5}
    expected_output = {
        "missing": {"d": 5},
        "new_data": {"a": 1},
        "different": {"c": (3, 4)},
    }
    assert dict_differences(dict1, dict2) == expected_output
