from nose.tools import eq_

from ..block import Block
from ..timestamp import Timestamp


def test_construction_and_values():
    flags = ["nocreate", "noedit"]
    duration = "24 years"
    expiration = Timestamp(1234567890)
    
    block = Block(flags, duration, expiration)
    
    eq_(block.flags, flags)
    eq_(block.duration, duration)
    eq_(block.expiration, expiration)
    
    eq_(block, Block(block))
    eq_(block, Block(block.to_json()))
