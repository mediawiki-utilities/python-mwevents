from .. import Timestamp, Unavailable, User
from ... import configuration
from ...util import split_page_name
from .event import Event
from .match import Match


class UserRegistered(Event):
    MATCHES = [Match("newusers", "newusers", False, "log"),
               Match("newusers", "create", False, "log"),
               Match("newusers", "create2", False, "log"),
               Match("newusers", "autocreate", False, "log"),
               Match("newusers", "byemail", False, "log")]
    __slots__ = ('action', 'new')
    def initialize(self, timestamp, user, comment, action, new):
        super().initialize(timestamp, user, comment)
        self.action = str(action)
        self.new = User(new)
        
    @classmethod
    def from_rc_doc(cls, rc_doc, config=configuration.DEFAULT):
        """
        Example:
            {
                "type": "log",
                "ns": 2,
                "title": "User:IntDebBall",
                "rcid": 616284425,
                "pageid": 0,
                "revid": 0,
                "old_revid": 0,
                "user": "IntDebBall",
                "userid": 20124261,
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2013-11-12T03:56:32Z",
                "comment": "",
                "logid": 52558177,
                "logtype": "newusers",
                "logaction": "create",
                "tags": []
            },
            {
                "type": "log",
                "ns": 2,
                "title": "User:Fredielyn Bucio",
                "rcid": 616279592,
                "pageid": 0,
                "revid": 0,
                "old_revid": 0,
                "user": "Palmville",
                "userid": 20124109,
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2013-11-12T03:19:42Z",
                "comment": "",
                "logid": 52557705,
                "logtype": "newusers",
                "logaction": "create2",
                "tags": []
            },
            {
                "type": "log",
                "ns": 2,
                "title": "User:Phillykidd",
                "rcid": 616286015,
                "pageid": 0,
                "revid": 0,
                "old_revid": 0,
                "user": "Callanecc",
                "userid": 20124315,
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2013-11-12T04:09:32Z",
                "comment": "Requested account at [[WP:ACC]], request #110880",
                "logid": 52558431,
                "logtype": "newusers",
                "logaction": "byemail",
                "tags": []
            }
        """
        if rc_doc['logaction'] == "create":
            registered_name = rc_doc['user']
            registered_id = rc_doc['userid']
        else: #doc['logaction'] in ("create2","byemail")
            nsname, registered_name = split_page_name(rc_doc['ns'],
                                                      rc_doc['title'])
            registered_id = Unavailable # Not available
        
        return cls(
            Timestamp(rc_doc['timestamp']),
            User(
                rc_doc.get('userid'),
                rc_doc.get('user')
            ),
            rc_doc.get('comment'),
            rc_doc['logaction'],
            User(
                registered_id,
                registered_name
            )
        )
        
    

Event.register(UserRegistered)
