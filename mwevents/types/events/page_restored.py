from .event import Event
from .match import Match


class PageRestored(Event):
    MATCHES = [Match("delete", "restore", False, "log")]
    __slots__ = ('old_page_id', 'page')
    def __init__(self, timestamp, user, comment, old_page_id, page):
        super().__init__(timestamp, user, comment)
        self.old_page_id = int(old_page_id) if old_page_id is not None else None
        self.page = Page(page)
    
    @classmethod
    def from_api_doc(cls, api_doc):
        """
        :Example API doc::
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
        ns, title = Page.parse_title(api_doc['title'])
        assert ns == api_doc['ns']
        
        return cls(
            Timestamp(api_doc['timestamp'])
            User(
                int(doc['userid']),
                doc['user']
            ),
            api_doc['comment'],
            None, # Not available
            Page(
                doc['pageid'],
                ns,
                title
            )
        )
    
    

# Event.register(RevisionSaved)
# TODO: Uncomment when ready
