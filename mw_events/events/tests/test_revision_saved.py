from nose.tools import eq_

from jsonable import JSONable

from ...types import Revision, Timestamp, User
from ..revision_saved import RevisionSaved


def test_construction_and_values():
    timestamp = Timestamp(1234567890)
    user = User(10, "Foobar!")
    comment = "This is a comment!"
            
    revision = Revision(10, 9, 100, "12345678901234567890123457890AB", 12,
                        False)
    revision_saved = RevisionSaved(timestamp, user, comment, revision)
    
    eq_(revision_saved.timestamp, timestamp)
    eq_(revision_saved.user, user)
    eq_(revision_saved.comment, comment)
    eq_(revision_saved.revision, revision)
