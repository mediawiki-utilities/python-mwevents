from .event import Event
from .match import Match


class PageProtectionModified(Event):
    MATCHES = [Match("protect", "protect", False, "log"),
               Match("protect", "modify", False, "log"),
               Match("protect", "unprotect", False, "log")]
    __slots__ = ('page', 'action', 'protection')
    def __init__(self, timestamp, user, comment, page, action, protections):
        super().__init__(timestamp, user, comment)
        self.page = Page(page)
        self.action = str(action)
        self.protections = [Protection(p) for p in protections]
        
    @classmethod
    def from_api_doc(cls, api_doc, config=configuration.DEFAULTS):
        """
        Example:
            {
                "type": "log",
                "ns": 0,
                "title": "Alice (Avril Lavigne song)",
                "rcid": 616736350,
                "pageid": 25727375,
                "revid": 0,
                "old_revid": 0,
                "user": "Mark Arsten",
                "userid": "15020596",
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2013-11-14T03:20:35Z",
                "comment": "Persistent IP edit warring",
                "logid": 52608670,
                "logtype": "protect",
                "logaction": "protect",
                "0": "\u200e[edit=autoconfirmed] (expires 03:20, 21 November 2013 (UTC))",
                "1": "",
                "tags": []
            }
            {
                "type": "log",
                "ns": 6,
                "title": "File:ElmerFlick.jpg",
                "rcid": 616706496,
                "pageid": 986245,
                "revid": 0,
                "old_revid": 0,
                "user": "DYKUpdateBot",
                "userid": "11745509",
                "bot": "",
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2013-11-14T00:05:14Z",
                "comment": "File off the [[T:DYK|DYK]] section of the Main Page",
                "logid": 52605770,
                "logtype": "protect",
                "logaction": "unprotect",
                "tags": []
            }
        """
        ns, title = config.title_parser.parse(api_doc['title'])
        assert ns == api_doc['ns']
        
        if api_doc['logaction'] in ("protect", "modify"):
            protections = Protection.from_params(doc.get('0'), config)
        elif api_doc['logaction'] == "unprotect":
            protections = []
        else:
            assert False, "Shouldn't happen."
        
        return cls(
            Timestamp(api_doc['comment']),
            User(
                int(api_doc['userid']),
                api_doc['user']
            )
            Page(
                api_doc['pageid'],
                api_doc['ns'],
                title
            ),
            protections
        )
    
# Event.register(PageProtectionModified)
# TODO: Uncomment when ready
