# -*- coding: utf-8 -*-


def test_remove_comments(wish):
    remove_comments = wish
    assert list(remove_comments('#')) == ['']
    assert list(remove_comments('#\n')) == ['']
    assert list(remove_comments('# comment\nnon comment')) == ['', 'non comment']
    assert list(remove_comments('# comment\nnon comment\n')) == ['', 'non comment']
