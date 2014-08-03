import json
import os.path

from nose.tools import eq_

from .. import Event, PageCreated, PageRestored, RevisionSaved
from ... import Page, Revision, Timestamp, Unavailable, User


def test_construction_and_values():
    timestamp = Timestamp(1234567890)
    user = User(10, "foobar")
    comment = "A sample comment that says some things."
    
    event = Event(timestamp, user, comment)
    
    eq_(event.timestamp, timestamp)
    eq_(event.user, user)
    eq_(event.comment, comment)
    
    eq_(event, Event(event))
    eq_(event, Event(event.to_json()))

def test_json_of_subclasses():
    user = User(10, "Foo")
    page = Page(12, 2, "Bar")
    timestamp = Timestamp(1234567890)
    revision = Revision(457863, 7328, 23423,
                        "1234567890123457890123457890ab", 12, False)
    events = [
        PageRestored(timestamp, user, "?", Unavailable, page),
        RevisionSaved(timestamp, user, "!", revision)
    ]
    
    docs = [e.to_json() for e in events]
    
    new_events = [Event(d) for d in docs]
    
    eq_(events, new_events)

def test_from_rc_doc_order():
    rc_doc = {
        "type": "new",
        "ns": 14,
        "title": "Category:Buildings and structures under " + \
                 "construction in Belgium",
        "pageid": 43457411,
        "revid": 619588219,
        "old_revid": 0,
        "rcid": 672727804,
        "user": "Vegaswikian",
        "userid": "214427",
        "oldlen": 0,
        "newlen": 137,
        "timestamp": "2014-08-02T20:07:22Z",
        "comment": "Add a series category",
        "sha1": "30f240252ca93e5830bef7f831fb8cb251cc4d72"
    }
    
    events = list(Event.from_rc_doc(rc_doc))
    
    eq_(len(events), 2)
    assert isinstance(events[0], PageCreated)
    assert isinstance(events[1], RevisionSaved)
    
    eq_(events[0].page.id, events[1].revision.page_id)


def test_from_rc_docs():
    f = open(os.path.join(os.path.dirname(__file__), "rc_docs.json"))
    
    rc_docs = json.load(f)
    
    events = list(event for rc_doc in rc_docs \
                        for event in Event.from_rc_doc(rc_doc))
    
    eq_(len(events), 51)
