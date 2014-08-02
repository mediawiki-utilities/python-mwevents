from .event import Event, Match


class UserUnblocked(Event):
    MATCHES = [MATCH("block", "unblock", False, "log")]
    __slots__ = ('unblocked',)
    def __init__(self, timestamp, user, comment, unblocked):
        super().__init__(timestamp, user, comment)
        self.unblocked = User(unblocked)
        
    
    @classmethod
    def from_api_doc(cls, api_doc, config):
        """
        Example:
            {
                "type": "log",
                "ns": 2,
                "title": "User:RYasmeen (WMF)",
                "rcid": 616266827,
                "pageid": 41055069,
                "revid": 0,
                "old_revid": 0,
                "user": "Risker",
                "userid": "726851",
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2013-11-12T01:48:22Z",
                "comment": "per [[https://en.wikipedia.org/wiki/User_talk:RYasmeen_%28WMF%29#Staff_account]]",
                "logid": 52556522,
                "logtype": "block",
                "logaction": "unblock",
                "tags": []
            }
        """
        ns, unblocked_name = config.title_parser.parse(api_doc['title'])
        assert ns == 2
        
        return cls(
            Timestamp(api_doc['timestamp'])
            User(
                api_doc['userid'],
                api_doc['user']
            ),
            api_doc['comment'],
            User(
                None, # Not available
                unblocked_name
            )
        )
    
Event.register(UserUnblocked)
