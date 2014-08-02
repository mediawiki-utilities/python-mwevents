from .event import Event, Match


class PageCreated(Event):
    MATCHES = [Match(None, None, True, "new", priority=25)]
    __slots__ = ('page',)
    def __init__(self, timestamp, user, comment, page):
        super().__init__(timestamp, user, comment)
        self.page = Page(page)
    
    @classmethod
    def from_api_doc(cls, api_doc, config=configuration.DEFAULTS):
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
        
        ns, title = config.title_parser.parse(api_doc['title'])
        assert ns == api_doc['ns']
        
        cls(
            Timestamp(api_doc['timestamp']),
            User(
                int(api_doc['userid']),
                api_doc['user']
            ),
            api_doc['comment'],
            Page(
                api_doc['page_id'],
                ns,
                title
            )
        )

# Event.register(PageCreated)
# TODO: Uncomment when ready
