import phpserialize

from .. import Page, Timestamp, Unavailable, User
from ... import configuration
from ...util import split_page_name
from .event import Event
from .match import Match


class PageMoved(Event):
    MATCHES = [Match("move", "move", False, "log"),
               Match("move", "move_redir", False, "log")]
    __slots__ = ('old', 'new')
    def initialize(self, timestamp, user, comment,
                         action, redirect_page_id, old, new):
        super().initialize(timestamp, user, comment)
        self.action = str(action)
        self.redirect_page_id = \
                Unavailable.otherwise(redirect_page_id, int) or 0
        self.old = Page(old)
        self.new = Page(new)
    
    @classmethod
    def from_rc_doc(cls, rc_doc, config=configuration.DEFAULT):
        """
        :Example API doc::
            {
                "type": "log",
                "ns": 15,
                "title": "Category talk:Joe 90 albums",
                "rcid": 616263570,
                "pageid": 41054940,
                "revid": 0,
                "old_revid": 0,
                "user": "Cydebot",
                "userid": "1215485",
                "bot": "",
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2013-11-12T01:29:15Z",
                "comment": "Robot - Speedily moving category Joe 90 albums to [[:Category:Joe 90 (band) albums]] per [[WP:CFDS|CFDS]].",
                "logid": 52556255,
                "logtype": "move",
                "logaction": "move",
                "move": {
                    "new_ns": 15,
                    "new_title": "Category talk:Joe 90 (band) albums"
                },
                "tags": []
            }
        """
        old_nsname, old_title = split_page_name(rc_doc['ns'], rc_doc['title'])
        
        new_nsname, new_title = split_page_name(rc_doc['move']['new_ns'],
                                                rc_doc['move']['new_title'])
        
        return cls(
            Timestamp(rc_doc['timestamp']),
            User(
                rc_doc.get('userid'),
                rc_doc.get('user')
            ),
            rc_doc.get('comment'),
            rc_doc['logaction'],
            rc_doc.get('pageid') or 0, # Note: Not the moved page_id.
            Page(
                Unavailable,
                rc_doc['ns'],
                old_title
            ),
            Page(
                Unavailable,
                rc_doc['move']['new_ns'],
                new_title
            )
        )


Event.register(PageMoved)
