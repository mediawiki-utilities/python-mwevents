from .event import Event
from .match import Match


class PageDeleted(Event):
    MATCHES = [Match("delete", "delete", False, "log")]
    __slots__ = ('page',)
    def __init__(self, timestamp, user, comment, page):
        super().__init__(timestamp, user, comment)
        self.page = Page(page)
    
    @classmethod
    def from_api_doc(cls, api_doc, config=DEFAULT_CONFIG):
        """
        :Example API doc::
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
        ns, title = config.title_parser.parse(api_doc['title'])
        assert ns == api_doc['ns']
        
        return cls(
            Timestamp('rc_timestamp'),
            User(
                int(api_doc['userid']),
                api_doc['user']
            ),
            api_doc['comment'],
            Page(
                api_doc['pageid'],
                ns,
                title
            )
        )
    
    @classmethod
    def from_db_row(cls, db_row, config=DEFAULT_CONFIG):
        """
        """
        ns, title = config.title_parser.parse(db_row['log_title'])
        assert ns == db_row['ns']
        
        return cls(
            Timestamp(db_row['log_timestamp']),
            User(
                int(db_row['log_user']),
                db_row['log_user_text']
            ),
            db_row['log_comment'],
            Page(
                db_row['log_page'], # Note, this is set to zero for old deleted
                                    # pages.
                ns,
                title
            )
        )
    
Event.register(PageDeleted)
