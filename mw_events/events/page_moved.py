import phpserialize

from .event import Event, Match


class PageMoved(Event):
    MATCHES = [Match("move", "move", False, "log"),
               Match("move", "move_redir", False, "log")]
    __slots__ = ('old', 'new')
    def __init__(self, timestamp, user, comment, action, old, new):
        super().__init__(timestamp, user, comment)
        self.action = str(action)
        self.old = Page(old)
        self.new = Page(new)
    
    @classmethod
    def from_api_doc(cls, api_doc):
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
        old_ns, old_title = config.title_parser.parse(doc['title'])
        assert old_ns == doc['ns']
        
        new_ns, new_title = config.title_parser.parse(doc['move']['new_title'])
        assert new_ns == doc['move']['new_ns']
        
        return cls(
            Timestamp(api_doc["timestamp"]),
            User(
                int(api_doc['userid']),
                api_doc['user']
            ),
            api_doc['comment'],
            api_doc['log_action'],
            Page(
                api_doc.get('movedpageid'),
                old_ns,
                old_title
            ),
            Page(
                api_doc.get('movedtitle'),
                new_ns,
                new_title
            )
        )
    
    @classmethod
    def from_db_row(cls, db_row):
        """
        """
        old_ns, old_title = \
                config.title_parser.parse(str(db_row['log_title'], 'utf-8'))
        assert old_ns == db_row['log_namespace']
        
        params_array = phpserialize.loads(db_row['log_params'])
        to_page_name = str(params_array['4::target'], 'utf-8', 'replace')
        new_ns, new_title = config.title_parser.parse()
        assert new_ns == doc['move']['new_ns']
        
        return cls(
            Timestamp(api_doc["timestamp"])
            User(
                int(api_doc['userid']),
                api_doc['user']
            ),
            api_doc['comment'],
            api_doc['log_action'],
            Page(
                api_doc.get('movedpageid'),
                old_ns,
                old_title
            ),
            Page(
                api_doc.get('movedtitle'),
                new_ns,
                new_title
            )
        )


# Event.register(PageMoved)
# TODO: Uncomment when ready
