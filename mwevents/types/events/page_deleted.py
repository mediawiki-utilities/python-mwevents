from .. import Page, Timestamp, Unavailable, User
from ... import configuration
from ...util import split_page_name
from .event import Event
from .match import Match


class PageDeleted(Event):
    MATCHES = [Match("delete", "delete", False, "log")]
    __slots__ = ('page',)
    def initialize(self, timestamp, user, comment, page):
        super().initialize(timestamp, user, comment)
        self.page = Page(page)
    
    @classmethod
    def from_rc_doc(cls, rc_doc, config=configuration.DEFAULT):
        """
        Example:
            {
                "type": "log",
                "ns": 15,
                "title": "Category talk:Joe songs",
                "rcid": 616263547,
                "pageid": 0,
                "revid": 0,
                "old_revid": 0,
                "user": "Cydebot",
                "userid": "1215485",
                "bot": "",
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2013-11-12T01:29:06Z",
                "comment": "Robot - Speedily moving category Joe songs to [[:Category:Joe (singer) songs]] per [[WP:CFDS|CFDS]].",
                "logid": 52556251,
                "logtype": "delete",
                "logaction": "delete",
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
            Page(
                rc_doc.get('pageid') or Unavailable, # For old entries,
                                                 # this is set to zero
                rc_doc['ns'],
                title
            )
        )
    
Event.register(PageDeleted)
