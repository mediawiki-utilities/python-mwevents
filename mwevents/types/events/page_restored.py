
from .. import Page, Timestamp, Unavailable, User
from ... import configuration
from ...util import split_page_name
from .event import Event
from .match import Match


class PageRestored(Event):
    MATCHES = [Match("delete", "restore", False, "log")]
    __slots__ = ('old_page_id', 'page')
    def initialize(self, timestamp, user, comment, old_page_id, page):
        super().initialize(timestamp, user, comment)
        self.old_page_id = Unavailable.otherwise(old_page_id, int)
        self.page = Page(page)
    
    @classmethod
    def from_rc_doc(cls, rc_doc, config=configuration.DEFAULT):
        """
        Example:
            {
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
        """
        nsname, title = split_page_name(rc_doc['ns'], rc_doc['title'])
        
        return cls(
            Timestamp(rc_doc['timestamp']),
            User(
                rc_doc.get('userid'),
                rc_doc.get('user')
            ),
            rc_doc.get('comment'),
            Unavailable, # Not available
            Page(
                rc_doc.get('pageid'),
                rc_doc.get('ns'),
                title
            )
        )
    
    

Event.register(PageRestored)
