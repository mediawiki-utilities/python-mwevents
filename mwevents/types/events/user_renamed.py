from ... import configuration
from .event import Event
from .match import Match
from .. import User, Timestamp, Unavailable


class UserRenamed(Event):
    """
    TODO: Figure out what to do with centralauth stuff.
    """
    MATCHES = [Match("renameuser", "renameuser", False, "log")]
    __slots__ = ('old', 'new')
    def initialize(self, timestamp, user, comment, old, new):
        super().initialize(timestamp, user, comment)
        self.old = User(old)
        self.new = User(new)
    
        
    @classmethod
    def from_api_doc(cls, api_doc, config=configuration.DEFAULT):
        """
        Example:
            {
                "type": "log",
                "ns": 2,
                "title": "User:Tuhin Karmakar",
                "rcid": 615891880,
                "pageid": 0,
                "revid": 0,
                "old_revid": 0,
                "user": "Andrevan",
                "userid": "13732",
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2013-11-10T12:04:41Z",
                "comment": "WP:CHU",
                "logid": 52520596,
                "logtype": "renameuser",
                "logaction": "renameuser",
                "olduser": "Tuhin Karmakar",
                "newuser": "Anonymous23648762289",
                "edits": 19,
                "tags": []
            }
        """
        return cls(
            Timestamp(rc_doc['timestamp']),
            User(
                rc_doc.get('userid'),
                rc_doc.get('user')
            ),
            rc_doc.get('comment'),
            User(
                Unavailable, #Not available
                doc['olduser']
            ),
            User(
                Unavailable, #Not available
                doc['newuser']
            )
        )

    @classmethod
    def from_rc_doc(cls, rc_doc, config=configuration.DEFAULT):
        """
        Example:
            {
                "logtype": "renameuser",
                "pageid": 0,
                "edits": 1,
                "userid": "1795359",
                "logid": 57568951,
                "logaction": "renameuser",
                "type": "log",
                "newuser": "Whitedr9gon",
                "comment": "user request",
                "newlen": 0,
                "ns": 2,
                "old_revid": 0,
                "rcid": 668780651,
                "title": "User:Tomahawke",
                "user": "Xeno",
                "oldlen": 0,
                "revid": 0,
                "olduser": "Tomahawke",
                "timestamp": "2014-07-14T13:22:06Z"
            }
        """
        return cls(
            Timestamp(rc_doc.get('timestamp')),
            User(
                rc_doc.get('userid'),
                rc_doc.get('user')
            ),
            rc_doc.get('comment'),
            User(
                Unavailable,  # Not available
                rc_doc.get('olduser')
            ),
            User(
                Unavailable,  # Not available
                rc_doc.get('newuser')
            )
        )


Event.register(UserRenamed)
