
def test_parse_bool(wish):
    parse_bool = wish

    assert not parse_bool('false')
    assert not parse_bool('FALSE')
    assert not parse_bool('0')

    assert parse_bool('true')
    assert parse_bool('TRUE')
    assert parse_bool('1')
