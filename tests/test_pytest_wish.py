# -*- coding: utf-8 -*-

import pytest_wish


TEST_FACTORIAL_PY = '''
def test_factorial(wish):
    factorial = wish
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(21) == 51090942171709440000
'''
TEST_FACTORIAL_TXT = '''
# test
math:fabs # comment
 math:factorial
math:dummy
dummy:dummy
'''


def test_import_coverage():
    """Fix the coverage by pytest-cov, that may trigger after pytest_wish is already imported."""
    from imp import reload  # Python 2 and 3 reload
    reload(pytest_wish)


def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'wish:',
        '*--wish-modules*',
        '*--wish-fail*',
    ])


def test_skip_wish(testdir):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    testdir.makepyfile(TEST_FACTORIAL_PY)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '-v',
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*test_factorial*wish*SKIPPED',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_wish_modules(testdir):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    testdir.makepyfile(TEST_FACTORIAL_PY)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--wish-modules=math',
        '-v',
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*test_factorial*math:fabs*xfail',
        '*test_factorial*math:factorial*XPASS',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_wish_modules_all(testdir):
    testdir.makepyfile(TEST_FACTORIAL_PY)
    result = testdir.runpytest(
        '--wish-modules=all',
        '--wish-includes=pip.exceptions',
        '-v',
    )
    result.stdout.fnmatch_lines([
        '*test_factorial*pip.exceptions:*xfail',
    ])
    assert result.ret == 0


def test_wish_fail(testdir):
    testdir.makepyfile(TEST_FACTORIAL_PY)
    result = testdir.runpytest(
        '--wish-modules=math',
        '--wish-fail',
        '-v',
    )
    result.stdout.fnmatch_lines([
        '*test_factorial*math:fabs*FAILED',
        '*test_factorial*math:factorial*PASSED',
    ])
    assert result.ret == 1


def test_wish_modules_object_blacklist(testdir):
    testdir.makepyfile(TEST_FACTORIAL_PY)
    result = testdir.runpytest(
        '--wish-modules=posix',
        '--wish-includes=.*exit',
        '-v',
    )
    assert result.ret == 0


def test_wish_objects(testdir):
    objects_txt = testdir.tmpdir.join('objects_txt')
    objects_txt.write(TEST_FACTORIAL_TXT)
    testdir.makepyfile(TEST_FACTORIAL_PY)
    result = testdir.runpytest(
        '--wish-objects={}'.format(objects_txt),
        '-v',
    )
    result.stdout.fnmatch_lines([
        '*test_factorial*math:fabs*xfail',
        '*test_factorial*math:factorial*XPASS',
    ])
    assert result.ret == 0
