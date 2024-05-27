def dict_differences(dict1: dict, dict2: dict) -> dict:
    """
    Given two dictionaries, returns the differences between them.

    Args:
        dict1 (dict): First dictionary.
        dict2 (dict): Second dictionary.

    Returns:
        dict: Dictionary containing missing, new_data, and different items.
    """

    missing = {k: dict2[k] for k in dict2 if k not in dict1}
    new_data = {k: dict1[k] for k in dict1 if k not in dict2}
    different = {
        k: (dict1[k], dict2[k]) for k in dict1 if k in dict2 and dict1[k] != dict2[k]
    }

    return {
        "missing": missing,
        "new_data": new_data,
        "different": different,
    }
