
import os

import pytest_nodev


@pytest_nodev.search('object_from_name')
def test_object_from_name_simple():
    assert object_from_name('os:O_CREAT') is os.O_CREAT
    assert object_from_name('os.path:join') is os.path.join
    assert object_from_name('builtins:True') is True
    assert object_from_name('builtins:open') is open


@pytest_nodev.search('object_from_name')
def test_object_from_name_pep3155():
    # instance methods compare by equality, see http://stackoverflow.com/questions/15977808
    assert object_from_name('os:O_CREAT.bit_length') == os.O_CREAT.bit_length
    assert object_from_name('builtins:int.bit_length') is int.bit_length
