import pytest

from nwcalc.addr_calc import *

@pytest.mark.parametrize(
    ('ipv4', 'expected'), [
        ('0.0.0.-1', False),
        ('0.0.0.0', True),
        ('192.0.2.1', True),
        ('255.255.255.255', True),
        ('255.255.255.256', False),
        ('255.255.255.', False),
        ('255.255.255.25 5', False),
        ('255.255.255.a', False),
        ('255.255.255.0255', False),
    ]
)

def test_ipv4_validate(ipv4, expected):
    assert ipv4_validate(ipv4) == expected

@pytest.mark.parametrize(
    ('ipv4_long', 'expected'), [
        (-1, False),
        (0, True),
        (1, True),
        (3232235521, True),
        (4294967295, True),
        (4294967296, False),
        ('323223552 1', False),
        ('323223552a', False),
        (32322355201, False),
    ]
)

def test_ipv4_size_check(ipv4_long, expected):
    assert ipv4_size_check(ipv4_long) == expected

@pytest.mark.parametrize(
    ('ipv4', 'expected'), [
        ('0.0.0.-1', False),
        ('0.0.0.0', 0),
        ('192.0.2.1', 3221225985),
        ('255.255.255.255', 4294967295),
        ('255.255.255.256', False),
        ('255.255.255.', False),
        ('255.255.255.25 5', False),
        ('255.255.255.a', False),
        ('255.255.255.0255', False),
    ]
)

def test_ipv42long(ipv4, expected):
    assert ipv42long(ipv4) == expected

@pytest.mark.parametrize(
    ('ipv4_long', 'expected'), [
        (-1, False),
        (0, '0.0.0.0'),
        (1, '0.0.0.1'),
        (3232235521, '192.168.0.1'),
        (4294967295, '255.255.255.255'),
        (4294967296, False),
        ('323223552 1', False),
        ('323223552a', False),
        (32322355201, False),
    ]
)

def test_long2ipv4(ipv4_long, expected):
    assert long2ipv4(ipv4_long) == expected
