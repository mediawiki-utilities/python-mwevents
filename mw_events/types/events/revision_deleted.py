from .event import Event, Match


class RevisionDeleted(Event):
    MATCHES = [Match("delete", "revision", True, "log")]
    __slots__ = ('revision',)
    def __init__(self, timestamp, user, comment, revision):
        super().__init__(timestamp, user, comment)
        self.revision = Revision(revision)
    
Event.EVENTS[RevisionDeleted] = RevisionDeleted
