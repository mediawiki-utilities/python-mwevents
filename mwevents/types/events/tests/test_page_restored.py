from nose.tools import eq_

from jsonable import JSONable

from ... import Page, Timestamp, Unavailable, User
from ..page_restored import PageRestored


def test_construction_and_values():
    timestamp = Timestamp(1234567890)
    user = User(10, "Foobar!")
    comment = "This is a comment!"
    
    old_page_id = 10
    page = Page(10, 2, "Foobar!")
    page_restored = PageRestored(timestamp, user, comment, old_page_id, page)
    
    eq_(page_restored.timestamp, timestamp)
    eq_(page_restored.user, user)
    eq_(page_restored.comment, comment)
    eq_(page_restored.old_page_id, old_page_id)
    eq_(page_restored.page, page)


def test_from_rc_doc():
    rc_doc = {
        "type": "log",
        "ns": 3,
        "title": "User talk:Envisage Drawn",
        "rcid": 616228397,
        "pageid": 41053035,
        "revid": 0,
        "old_revid": 0,
        "user": "Peridon",
        "userid": "7128128",
        "oldlen": 0,
        "newlen": 0,
        "timestamp": "2013-11-11T22:01:52Z",
        "comment": "1 revision restored: wrong button!",
        "logid": 52553202,
        "logtype": "delete",
        "logaction": "restore",
        "tags": []
    }
    
    page_restored = PageRestored.from_rc_doc(rc_doc)
    
    eq_(page_restored.timestamp, Timestamp(rc_doc['timestamp']))
    eq_(page_restored.user, User(rc_doc['userid'], rc_doc['user']))
    eq_(page_restored.comment, rc_doc['comment'])
    eq_(page_restored.old_page_id, Unavailable)
    eq_(page_restored.page.id, rc_doc['pageid'])
    eq_(page_restored.page.namespace, rc_doc['ns'])
