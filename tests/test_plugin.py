# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Alessandro Amici
#

# python 2 support via python-future
from __future__ import absolute_import, unicode_literals


from pytest_nodev import plugin


TEST_PASS_PY = '''
def test_pass():
    assert True
'''
TEST_FACTORIAL_PY = '''
def test_factorial(candidate):
    factorial = candidate
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(21) == 51090942171709440000
'''
TEST_POW_PY = '''
import pytest
@pytest.mark.candidate('pow')
def test_pow():
    assert pow(2, 9, 47) == 42
'''


def test_import_coverage():
    """Fix the coverage by pytest-cov, that may trigger after pytest_nodev is already imported."""
    from imp import reload  # Python 2 and 3 reload
    reload(plugin)


#
# pytest hooks
#
def test_pytest_addoption(testdir):
    """The plugin is registered with pytest."""
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'nodev:',
        '*--candidates-from-stdlib*',
        '*--candidates-fail*',
    ])


def test_pytest_generate_tests(testdir):
    testdir.makepyfile(TEST_FACTORIAL_PY + TEST_PASS_PY)
    result = testdir.runpytest(
        '--candidates-from-modules=math',
        '-v',
    )
    result.stdout.fnmatch_lines([
        '*test_factorial*math:factorial*XPASS',
        '*test_pass*PASSED',
    ])
    assert result.ret == 0

    result = testdir.runpytest(
        '--candidates-from-modules=math',
        '--candidates-fail',
        '-v',
    )
    result.stdout.fnmatch_lines([
        '*test_factorial*math:factorial*PASSED',
        '*test_pass*PASSED',
    ])
    assert result.ret == 1


def test_pytest_terminal_summary(testdir):
    testdir.makepyfile(TEST_PASS_PY)
    result = testdir.runpytest(
        '-v'
    )
    result.stdout.fnmatch_lines([
        '*test_pass*PASSED',
    ])
    assert result.ret == 0

    testdir.makepyfile(TEST_FACTORIAL_PY)
    result = testdir.runpytest(
        '--candidates-from-modules=math',
    )
    result.stdout.fnmatch_lines([
        '*test_factorial*math:factorial*PASSED',
    ])
    assert result.ret == 0


#
# command line options
#
def test_pytest_run_no_candidate(testdir):
    """We didn't break pytest."""
    testdir.makepyfile(TEST_PASS_PY)
    result = testdir.runpytest(
        '-v',
    )
    result.stdout.fnmatch_lines([
        '*test_pass*PASSED',
    ])
    assert result.ret == 0


def test_pytest_run_no_candidate_option(testdir):
    """Skip tests with the *candidate* fixture if no ``--candidates-*`` option is given."""
    testdir.makepyfile(TEST_FACTORIAL_PY)
    result = testdir.runpytest(
        '-v',
    )
    result.stdout.fnmatch_lines([
        '*test_factorial*candidate*SKIPPED',
    ])
    assert result.ret == 0


def test_pytest_run_from_modules(testdir):
    testdir.makepyfile(TEST_FACTORIAL_PY)
    result = testdir.runpytest(
        '--candidates-from-modules=math',
        '-v',
    )
    result.stdout.fnmatch_lines([
        '*test_factorial*math:fabs*xfail',
        '*test_factorial*math:factorial*XPASS',
    ])
    assert result.ret == 0


def test_pytest_run_from_modules_twice(testdir):
    testdir.makepyfile(TEST_FACTORIAL_PY + TEST_POW_PY)
    result = testdir.runpytest(
        '--candidates-from-modules=math',
        '-v',
    )
    result.stdout.fnmatch_lines([
        '*test_factorial*math:fabs*xfail',
        '*test_factorial*math:factorial*XPASS',
    ])
    assert result.ret == 0


def test_pytest_run_from_specs(testdir):
    testdir.makepyfile(TEST_FACTORIAL_PY)
    result = testdir.runpytest(
        '--candidates-from-specs=pip',
        '--candidates-includes=pip.exceptions',
        '-v',
    )
    result.stdout.fnmatch_lines([
        '*test_factorial*pip.exceptions:*xfail',
    ])
    assert result.ret == 0


def test_pytest_run_from_stdlib(testdir):
    testdir.makepyfile(TEST_FACTORIAL_PY)
    result = testdir.runpytest(
        '--candidates-from-stdlib',
        '--candidates-includes=math',
        '-v',
    )
    result.stdout.fnmatch_lines([
        '*test_factorial*math:fabs*xfail',
        '*test_factorial*math:factorial*XPASS',
    ])
    assert result.ret == 0


def test_pytest_run_from_all(testdir, monkeypatch):
    testdir.makepyfile(TEST_FACTORIAL_PY)
    result = testdir.runpytest(
        '--candidates-from-all',
        '--candidates-includes=math:factorial|pip.exceptions',
        '-v',
    )
    assert result.ret == 1

    monkeypatch.setenv('PYTEST_NODEV_MODE', 'FEARLESS')
    result = testdir.runpytest(
        '--candidates-from-all',
        '--candidates-includes=math:factorial|pip.exceptions',
        '-v',
    )
    result.stdout.fnmatch_lines([
        '*test_factorial*math:factorial*XPASS',
        '*test_factorial*pip.exceptions:*xfail',
    ])
    assert result.ret == 0


def test_candidate_modules_object_blacklist(testdir):
    testdir.makepyfile(TEST_FACTORIAL_PY)
    result = testdir.runpytest(
        '--candidates-from-modules=posix',
        '--candidates-includes=.*fork',
        '-v',
    )
    assert result.ret == 0
