from fuzzywuzzy import fuzz as matcher, process


def matching(str1: str, str2: str):
    """
    Using levenshtein ratio and distance.
    return ratio in 0-100.
    """
    return matcher.ratio(str1, str2)


def matching_partial(str1: str, str2: str):
    """
    Using levenshtein ratio and distance.
    return ratio in 0-100.
    """
    return matcher.partial_ratio(str1, str2)


def get_most_matching(string: str, options: list):
    """
    Using levenshtein ratio and distance.
    return ratio tuple(most_matched_string, ratio)
    """
    return process.extractOne(string, options)
