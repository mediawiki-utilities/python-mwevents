from nose.tools import eq_

from ..protection import Protection
from ..timestamp import Timestamp


def test_construction_and_values():
    action = "edit"
    group = "sysop"
    expiration = None
    
    protection = Protection(action, group, expiration)
    
    eq_(protection.action, action)
    eq_(protection.group, group)
    eq_(protection.expiration, expiration)
    
    eq_(protection, Protection(protection.to_json()))
    

def test_from_params():
    log_params = (
        "[edit=autoconfirmed] (expires 23:31, 13 February 2009 (UTC)) " +
        "[move=autoconfirmed] (indefinite)\n"
    )
    
    eq_(
        [
            Protection("edit", "autoconfirmed",
                       Timestamp("2009-02-13T23:31:00Z")),
            Protection("move", "autoconfirmed", None),
        ],
        list(Protection.from_params(log_params))
    )
