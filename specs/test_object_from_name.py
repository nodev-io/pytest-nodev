import os


def test_object_from_name_simple(candidate):
    object_from_name = candidate
    assert object_from_name('os:O_CREAT') is os.O_CREAT
    assert object_from_name('os.path:join') is os.path.join
    assert object_from_name('builtins:True') is True
    assert object_from_name('builtins:open') is open


def test_object_from_name_pep3155(candidate):
    object_from_name = candidate
    # instance methods compare by equality, see http://stackoverflow.com/questions/15977808
    assert object_from_name('os:O_CREAT.bit_length') == os.O_CREAT.bit_length
    assert object_from_name('builtins:int.bit_length') is int.bit_length
