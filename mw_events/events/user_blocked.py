from .event import Event, Match


class UserBlocked(Event):
    MATCHES = [MATCH("block", "block", False, "log"),
               MATCH("block", "reblock", False, "log")]
    __slots__ = ('block',)
    def __init__(self, timestamp, user, comment, block):
        super().__init__(timestamp, user, comment)
        self.block = Block(block)
    
# Event.register(UserBlocked)
# TODO: Uncomment when ready
