# -*- coding: utf-8 -*-


def test_factorial(wish):
    factorial = wish
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(21) == 51090942171709440000
