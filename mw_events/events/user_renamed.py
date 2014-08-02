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
    
# Event.register(UserRenamed)
# TODO: Uncomment when ready
