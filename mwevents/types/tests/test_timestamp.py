from nose.tools import eq_

from ..timestamp import Timestamp


def test_construction_and_values():
    unix = 1234567890
    expected_json = "20090213233130"
    timestamp = Timestamp(unix)
    
    eq_(timestamp.unix(), unix)
    eq_(timestamp.to_json(), expected_json)
    
    eq_(timestamp, Timestamp(timestamp))
    eq_(timestamp, Timestamp(timestamp.to_json()))
