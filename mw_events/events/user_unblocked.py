from .event import Event, Match


class UserUnblocked(Event):
    MATCHES = [MATCH("block", "unblock", False, "log")]
    __slots__ = tuple()
    def __init__(self, timestamp, user, comment):
        super().__init__(timestamp, user, comment)
    
Event.EVENTS[UserUnblocked] = UserUnblocked
