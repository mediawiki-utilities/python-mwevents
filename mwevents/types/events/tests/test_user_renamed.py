from nose.tools import eq_

from ..user_renamed import UserRenamed
from ... import Timestamp, User, Unavailable


def test_from_rc_doc():
    rc_doc = {
        'type': 'log',
        'ns': 2,
        'title': 'User:Tuhin Karmakar',
        'rcid': 615891880,
        'pageid': 0,
        'revid': 0,
        'old_revid': 0,
        'user': 'Andrevan',
        'userid': '13732',
        'oldlen': 0,
        'newlen': 0,
        'timestamp': '2013-11-10T12:04:41Z',
        'comment': 'WP:CHU',
        'logid': 52520596,
        'logtype': 'renameuser',
        'logaction': 'renameuser',
        'olduser': 'Tuhin Karmakar',
        'newuser': 'Anonymous23648762289',
        'edits': 19,
        'tags': []
    }

    user_renamed = UserRenamed.from_rc_doc(rc_doc)

    eq_(user_renamed.timestamp, Timestamp(rc_doc['timestamp']))
    eq_(user_renamed.user, User(rc_doc['userid'], rc_doc['user']))
    eq_(user_renamed.comment, rc_doc['comment'])
    eq_(user_renamed.old, User(Unavailable, rc_doc['olduser']))
    eq_(user_renamed.new, User(Unavailable, rc_doc['newuser']))
