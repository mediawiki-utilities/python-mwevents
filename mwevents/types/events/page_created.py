from .. import Page, Timestamp, User
from ... import configuration
from ...util import split_page_name
from .event import Event
from .match import Match


class PageCreated(Event):
    MATCHES = [Match(None, None, True, "new")]
    PRIORITY = 50 # Must happen before RevisionSaved
    __slots__ = ('page',)
    def initialize(self, timestamp, user, comment, page):
        super().initialize(timestamp, user, comment)
        self.page = Page(page)
    
    @classmethod
    def from_rc_doc(cls, rc_doc, config=configuration.DEFAULT):
        """
        Example:
            {
                "type": "new",
                "ns": 1,
                "title": "Talk:Africa Movie Academy Award for Best Film by an African Living Abroad",
                "pageid": 43452004,
                "revid": 619486495,
                "old_revid": 0,
                "rcid": 672566259,
                "user": "Jamie Tubers",
                "userid": "14285562",
                "oldlen": 0,
                "newlen": 233,
                "timestamp": "2014-08-01T23:35:20Z",
                "comment": "[[WP:AES|\u2190]]Created page with '{{WikiProjectBannerShell|1= {{WikiProject Film|Awards-task-force=yes|class=list}} {{WikiProject Lists|class=List|importance=high}} {{WikiProject Awards|class=Lis...'",
                "tags": [],
                "sha1": "ecb44405afe0d2c5460841bf08fd8f9c44c86ce4"
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
                rc_doc.get('pageid'),
                rc_doc['ns'],
                title
            )
        )

Event.register(PageCreated)
