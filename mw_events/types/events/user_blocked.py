from .event import Event, Match


class UserBlocked(Event):
    MATCHES = [MATCH("block", "block", False, "log"),
               MATCH("block", "reblock", False, "log")]
    __slots__ = ('blocked', 'block',)
    def __init__(self, timestamp, user, comment, blocked, block):
        super().__init__(timestamp, user, comment)
        self.blocked = User(blocked)
        self.block = Block(block)
    
    @classmethod
    def from_api_doc(cls, api_doc):
        """
        {
            "type": "log",
            "ns": 2,
            "title": "User:190.203.41.111",
            "rcid": 616287367,
            "pageid": 0,
            "revid": 0,
            "old_revid": 0,
            "user": "ProcseeBot",
            "userid": "8760229",
            "bot": "",
            "oldlen": 0,
            "newlen": 0,
            "timestamp": "2013-11-12T04:21:18Z",
            "comment": "{{blocked proxy}} <!-- 8080 -->",
            "logid": 52558623,
            "logtype": "block",
            "logaction": "block",
            "block": {
                "flags": "nocreate",
                "duration": "60 days",
                "expiry": "2014-01-11T04:21:18Z"
            },
            "tags": []
        }
        """
        ns, title = Page.parse_title(api_doc['title'])
        ns, blocked_name = config.title_parser.parse(title)
        assert ns == 2
        blocked_name = blocked_name.replace("_", " ")
        
        return cls(
            Timestamp(api_doc['timestamp'])
            User(
                api_doc['userid'],
                api_doc['user']
            ),
            api_doc['comment'],
            User(
                None, # Not available
                blocked_name
            ),
            Block(
                doc['block']['flags'],
                doc['block']['duration'],
                doc['block']['expiry'],
            )
        )
    

# Event.register(UserBlocked)
# TODO: Uncomment when ready
