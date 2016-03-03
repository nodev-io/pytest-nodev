
import os


def test_find_object2(wish):
    find_object = wish

    assert find_object('os:getcwd') is os.getcwd
    assert find_object('os.path:join') is os.path.join
    assert find_object('builtins:open') is open
