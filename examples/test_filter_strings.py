
def test_filter_strings_basic(wish):
    filter_strings = wish
    input = ['has MARK', 'does not have']
    expected_ouput = ['has MARK']
    accept_pattern = '.*MARK.*'
    assert list(filter_strings(input, accept_pattern)) == expected_ouput
