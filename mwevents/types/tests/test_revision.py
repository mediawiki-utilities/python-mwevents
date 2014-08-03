from nose.tools import eq_

from ..revision import Revision
from ..unavailable import Unavailable


def test_construction_and_values():
    id = 129
    parent_id = 105
    bytes = 2324
    sha1 = "1234567890123457890123457890ab"
    page_id = 12
    minor = False
    
    revision = Revision(id, parent_id, bytes, sha1, page_id, minor)
    
    eq_(revision.id, id)
    eq_(revision.parent_id, parent_id)
    eq_(revision.bytes, bytes)
    eq_(revision.sha1, sha1)
    eq_(revision.page_id, page_id)
    eq_(revision.minor, minor)
    
    eq_(revision, Revision(revision))
    eq_(revision, Revision(revision.to_json()))

def test_unavailable_values():
    id = 129
    parent_id = None
    bytes = 2324
    sha1 = Unavailable
    page_id = 12
    minor = Unavailable
    
    revision = Revision(id, parent_id, bytes, sha1, page_id, minor)
    
    eq_(revision.id, id)
    eq_(revision.parent_id, 0) # Should convert None to zero
    eq_(revision.bytes, bytes)
    eq_(revision.sha1, sha1)
    eq_(revision.page_id, page_id)
    eq_(revision.minor, minor)
    
    eq_(revision, Revision(revision))
    eq_(revision, Revision(revision.to_json()))
    
    id = None
    parent_id = 105
    bytes = Unavailable
    sha1 = "1234567890123457890123457890ab"
    page_id = Unavailable
    minor = False

    revision = Revision(id, parent_id, bytes, sha1, page_id, minor)

    eq_(revision.id, id)
    eq_(revision.parent_id, parent_id)
    eq_(revision.bytes, bytes)
    eq_(revision.sha1, sha1)
    eq_(revision.page_id, page_id)
    eq_(revision.minor, minor)

    eq_(revision, Revision(revision))
    eq_(revision, Revision(revision.to_json()))
