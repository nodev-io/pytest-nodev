"""This module holds custom assertions for pytest-wish"""


def permutated_assert(*called_and_expecteds):
    """this function asserts that there has been a correct result for each invocation.

    and that the correct results are from the same argument permutation."""
    indexes = []
    for called, expected in called_and_expecteds:
        here_indexes = []
        assert expected in called.results
        for index, result in enumerate(called.results):
            if result == expected:
                here_indexes.append(index)
        indexes.append(set(here_indexes))
    if not set.intersection(*indexes):
        raise AssertionError('No single invocation with passed all tests')
