# -*- coding: utf-8 -*-


def test_find_exepath(wish):
    find_exepath = wish
    assert find_exepath('echo') == '/bin/echo'
    assert find_exepath('mount') == '/sbin/mount'
    assert find_exepath('grep') == '/usr/bin/grep'
