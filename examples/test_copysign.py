# -*- coding: utf-8 -*-
import pytest
from pytest_wish.assertions import permutated_assert


def test_relation1(wish_permutate_args):
    relation = wish_permutate_args
    permutated_assert([relation(1, 20), 1],
                      [relation(180, -2), -180])

    with pytest.raises(AssertionError) as excinfo:
        permutated_assert([relation(1, 20), 1],
                          [relation(180, -2), -180],
                          [relation(180, -2), 2])


def test_relation2(wish_permutate_args):
    relation = wish_permutate_args
    permutated_assert([relation(20, 1), 1],
                      [relation(-180, -2), -2],
                      [relation(180, -2), 2])
