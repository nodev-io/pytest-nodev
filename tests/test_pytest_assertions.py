from math import pow

from pytest import raises

from pytest_wish import assertions, utils


def test_permutated_assert():
    decorated_pow = utils.permutate_decorator(pow)
    assertions.permutated_assert(
        [decorated_pow(2, 3), 8],
        [decorated_pow(2, 4), 16],
        [decorated_pow(2, 5), 32],
    )
    assertions.permutated_assert(
        [decorated_pow(2, 3), 9],
        [decorated_pow(2, 4), 16],
        [decorated_pow(2, 5), 25],
    )
    with raises(AssertionError):
        assertions.permutated_assert(
            [decorated_pow(2, 3), 8],
            [decorated_pow(2, 5), 25],
        )
