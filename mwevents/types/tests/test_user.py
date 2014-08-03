from nose.tools import eq_

from ..unavailable import Unavailable
from ..user import User


def test_construction_and_values():
    id = 129
    text = "I am a username"
    
    user = User(id, text)
    
    eq_(user.id, id)
    eq_(user.text, text)
    
    eq_(user, User(user))
    eq_(user, User(user.to_json()))

def test_unavailable_id():
    
    id = Unavailable
    text = "I am a username"
    
    user = User(id, text)
    
    eq_(user.id, id)
    eq_(user.text, text)
    
    eq_(user, User(user))
    eq_(user, User(user.to_json()))
