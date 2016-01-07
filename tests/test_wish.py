# -*- coding: utf-8 -*-

TEST_FACTORIAL = """
def test_factorial(wish):
    assert wish(0) == 1
    assert wish(1) == 1
    assert wish(21) == 51090942171709440000
"""


def test_generate_tests(testdir):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    testdir.makepyfile(TEST_FACTORIAL)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--wish-modules=math',
        '-v',
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_factorial*math:factorial*XPASS',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_skip_tests(testdir):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    testdir.makepyfile(TEST_FACTORIAL)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '-v',
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_factorial*wish*SKIPPED',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


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
