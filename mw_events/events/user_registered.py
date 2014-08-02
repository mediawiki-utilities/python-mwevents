from .event import Event, Match


class UserRegistered(Event):
    MATCHES = [Match("newusers", "newusers", False, "log"),
               Match("newusers", "create", False, "log"),
               Match("newusers", "create2", False, "log"),
               Match("newusers", "autocreate", False, "log"),
               Match("newusers", "byemail", False, "log")]
    __slots__ = ('action', 'newuser')
    def __init__(self, timestamp, user, comment, action, newuser):
        super().__init__(timestamp, user, comment)
        self.action = str(action)
        self.newuser = User(newuser)
    
# Event.register(UserRegistered)
# TODO: Uncomment when ready
