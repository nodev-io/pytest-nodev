# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Alessandro Amici
#

# python 2 support via python-future
from __future__ import absolute_import, unicode_literals

import inspect


def search(target_name):
    def wish_decorator(test_func):
        def wish_wrapper(wish, monkeypatch, *args, **kwargs):
            if '.' in target_name:
                monkeypatch.setattr(target_name, wish, raising=False)
            else:
                monkeypatch.setattr(inspect.getmodule(test_func), target_name, wish, raising=False)
            return test_func(*args, **kwargs)
        return wish_wrapper
    return wish_decorator
