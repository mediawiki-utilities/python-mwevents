from nose.tools import eq_

from jsonable import JSONable

from ... import Revision, Timestamp, Unavailable, User
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

def test_from_rc_doc():
    rc_doc = {
        "type": "edit",
        "ns": 1,
        "title": "Talk:Neutral mutation",
        "rcid": 616266829,
        "pageid": 5555386,
        "revid": 581269873,
        "old_revid": 581268750,
        "user": "Grabriggs",
        "userid": "19701352",
        "oldlen": 23767,
        "newlen": 24046,
        "timestamp": "2013-11-12T01:48:22Z",
        "comment": "/* Neutral theory */",
        "tags": [],
        "sha1": "8817b4efd42c936254dfb09ce5bbfd0e4f9b848a"
    }
    
    revision_saved = RevisionSaved.from_rc_doc(rc_doc)
    
    eq_(revision_saved.timestamp, Timestamp(rc_doc['timestamp']))
    eq_(revision_saved.user, User(rc_doc['userid'], rc_doc['user']))
    eq_(revision_saved.comment, rc_doc['comment'])
    eq_(revision_saved.revision.bytes, rc_doc['newlen'])
    eq_(revision_saved.revision.sha1, rc_doc['sha1'])
    eq_(revision_saved.revision.page_id, rc_doc['pageid'])
    eq_(revision_saved.revision.minor, 'minor' in rc_doc)

def test_from_rev_doc():
    rev_doc = {
        "revid": 619093743,
        "parentid": 618899706,
        "user": "Eduen",
        "userid": 7527773,
        "timestamp": "2014-07-30T07:26:05Z",
        "size": 181115,
        "sha1": "c6236e5ad7b6af7c353a43ded631298c2b7e95ea",
        "contentmodel": "wikitext",
        "comment": "another quote from a prominent anarchist theroy which talks againts the simplification of a libertarian society to simply the absence of a state",
        "page": {
            "pageid": 12,
            "ns": 0,
            "title": "Anarchism"
        }
    }
    
    revision_saved = RevisionSaved.from_rev_doc(rev_doc)
    
    eq_(revision_saved.timestamp, Timestamp(rev_doc['timestamp']))
    eq_(revision_saved.user, User(rev_doc['userid'], rev_doc['user']))
    eq_(revision_saved.comment, rev_doc['comment'])
    eq_(revision_saved.revision.sha1, rev_doc['sha1'])
    eq_(revision_saved.revision.page_id, rev_doc['page']['pageid'])

def test_from_rc_row():
    rc_row = {
        'rc_id': 624362534,
        'rc_timestamp': "20131219020516",
        'rc_cur_time': "",
        'rc_user': 16380370,
        'rc_user_text': "RedVanderwall",
        'rc_namespace': 0,
        'rc_title': "Narragansett_Race_Track",
        'rc_comment': "/* The Biscuit */",
        'rc_minor': 1,
        'rc_bot': 0,
        'rc_new': 0,
        'rc_cur_id': 10680758,
        'rc_this_oldid': 586726430,
        'rc_last_oldid': 586725822,
        'rc_type': 0,
        'rc_source': "mw.edit",
        'rc_moved_to_ns': 0,
        'rc_moved_to_title': "",
        'rc_patrolled': 0,
        'rc_ip': "<redacted>",
        'rc_old_len': 24309,
        'rc_new_len': 24348,
        'rc_deleted': 0,
        'rc_logid': 0,
        'rc_log_type': None,
        'rc_log_action': "",
        'rc_params': ""
    }
    
    revision_saved = RevisionSaved.from_rc_row(rc_row)
    
    eq_(revision_saved.timestamp, Timestamp(rc_row['rc_timestamp']))
    eq_(revision_saved.user, User(rc_row['rc_user'], rc_row['rc_user_text']))
    eq_(revision_saved.comment, rc_row['rc_comment'])
    eq_(revision_saved.revision.sha1, Unavailable)
    eq_(revision_saved.revision.page_id, rc_row['rc_cur_id'])

def test_from_rev_row():
    rev_row = {
        'rev_id': 233192,
        'rev_page': 10,
        'rev_text_id': 233192,
        'rev_comment': "*",
        'rev_user': 99,
        'rev_user_text': "RoseParks",
        'rev_timestamp': "20010121021221",
        'rev_minor_edit': 0,
        'rev_deleted': 0,
        'rev_len': 124,
        'rev_parent_id': 0,
        'rev_sha1': "8kul9tlwjm9oxgvqzbwuegt9b2830vw"
    }
    
    revision_saved = RevisionSaved.from_rev_row(rev_row)
    
    eq_(revision_saved.timestamp, Timestamp(rev_row['rev_timestamp']))
    eq_(revision_saved.user,
        User(rev_row['rev_user'], rev_row['rev_user_text']))
    eq_(revision_saved.comment, rev_row['rev_comment'])
    eq_(revision_saved.revision.sha1, rev_row['rev_sha1'])
    eq_(revision_saved.revision.page_id, rev_row['rev_page'])
