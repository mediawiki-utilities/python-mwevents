from nose.tools import eq_

from ..unavailable import Unavailable


def test_otherwise():
    eq_(Unavailable, Unavailable.otherwise(Unavailable, int))
    eq_(None, Unavailable.otherwise(None, int))
    eq_(10, Unavailable.otherwise(10, int))
    eq_(10, Unavailable.otherwise("10", int))
