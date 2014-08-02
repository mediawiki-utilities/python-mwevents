from .event import Event, Match


class UserRenamed(Event):
    """
    TODO: Figure out what to do with centralauth stuff.
    """
    MATCHES = [MATCH("renameuser", "renameuser", False, "log")]
    __slots__ = ('old', 'new')
    def __init__(self, timestamp, user, comment, old, new):
        super().__init__(timestamp, user, comment)
        self.old = User(old)
        self.new = User(new)
    
        
    @classmethod
    def from_api_doc(cls, api_doc):
        """
        Example:
            {
                "type": "log",
                "ns": 2,
                "title": "User:Tuhin Karmakar",
                "rcid": 615891880,
                "pageid": 0,
                "revid": 0,
                "old_revid": 0,
                "user": "Andrevan",
                "userid": "13732",
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2013-11-10T12:04:41Z",
                "comment": "WP:CHU",
                "logid": 52520596,
                "logtype": "renameuser",
                "logaction": "renameuser",
                "olduser": "Tuhin Karmakar",
                "newuser": "Anonymous23648762289",
                "edits": 19,
                "tags": []
            }
        """
        return cls(
            Timestamp(doc['timestamp']),
            User(
                int(doc['userid']),
                doc['user']
            ),
            doc['comment'],
            User(
                None, #Not available
                doc['olduser']
            ),
            User(
                None, #Not available
                doc['newuser']
            )
        )
    
# Event.register(UserRenamed)
# TODO: Uncomment when ready
