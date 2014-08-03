from .. import Timestamp, Unavailable, User
from ... import configuration
from ...util import split_page_name
from .event import Event
from .match import Match


class UserUnblocked(Event):
    MATCHES = [Match("block", "unblock", False, "log")]
    __slots__ = ('unblocked',)
    def initialize(self, timestamp, user, comment, unblocked):
        super().initialize(timestamp, user, comment)
        self.unblocked = User(unblocked)
        
    
    @classmethod
    def from_rc_doc(cls, rc_doc, config=configuration.DEFAULT):
        """
        Example:
            {
                "type": "log",
                "ns": 2,
                "title": "User:RYasmeen (WMF)",
                "rcid": 616266827,
                "pageid": 41055069,
                "revid": 0,
                "old_revid": 0,
                "user": "Risker",
                "userid": "726851",
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2013-11-12T01:48:22Z",
                "comment": "per [[https://en.wikipedia.org/wiki/User_talk:RYasmeen_%28WMF%29#Staff_account]]",
                "logid": 52556522,
                "logtype": "block",
                "logaction": "unblock",
                "tags": []
            }
        """
        nsname, unblocked_name = split_page_name(rc_doc['ns'], rc_doc['title'])
        
        return cls(
            Timestamp(rc_doc['timestamp']),
            User(
                rc_doc.get('userid'),
                rc_doc.get('user')
            ),
            rc_doc.get('comment'),
            User(
                Unavailable, # Not available
                unblocked_name
            )
        )
    
Event.register(UserUnblocked)
