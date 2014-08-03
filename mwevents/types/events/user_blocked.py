from .. import Block, Timestamp, User
from ... import configuration
from ...util import split_page_name
from .event import Event
from .match import Match


class UserBlocked(Event):
    MATCHES = [Match("block", "block", False, "log"),
               Match("block", "reblock", False, "log")]
    __slots__ = ('blocked', 'block',)
    def initialize(self, timestamp, user, comment, blocked, block):
        super().initialize(timestamp, user, comment)
        self.blocked = User(blocked)
        self.block = Block(block)
    
    @classmethod
    def from_rc_doc(cls, rc_doc, config=configuration.DEFAULT):
        """
        {
            "type": "log",
            "ns": 2,
            "title": "User:190.203.41.111",
            "rcid": 616287367,
            "pageid": 0,
            "revid": 0,
            "old_revid": 0,
            "user": "ProcseeBot",
            "userid": "8760229",
            "bot": "",
            "oldlen": 0,
            "newlen": 0,
            "timestamp": "2013-11-12T04:21:18Z",
            "comment": "{{blocked proxy}} <!-- 8080 -->",
            "logid": 52558623,
            "logtype": "block",
            "logaction": "block",
            "block": {
                "flags": "nocreate",
                "duration": "60 days",
                "expiry": "2014-01-11T04:21:18Z"
            },
            "tags": []
        }
        """
        nsname, blocked_name = split_page_name(rc_doc['ns'], rc_doc['title'])
        
        if len(rc_doc['block'].get('flags', "")) > 0:
            flags = rc_doc['block']['flags'].split(",")
        else:
            flags = []
        
        return cls(
            Timestamp(rc_doc['timestamp']),
            User(
                rc_doc.get('userid'),
                rc_doc.get('user')
            ),
            rc_doc.get('comment'),
            User(
                None, # Not available
                blocked_name
            ),
            Block(
                flags,
                rc_doc['block']['duration'],
                rc_doc['block'].get('expiry'),
            )
        )
    

Event.register(UserBlocked)
