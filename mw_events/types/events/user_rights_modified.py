from .event import Event


class UserRightsModified(Event):
    __slots__ = ('modified', 'rights')
    def initialize(self, timestamp, user, comment, modified_user, old, new):
        super().initialize(timestamp, user, comment)
        
        self.modified_user = User(modified_user)
        self.old = Rights(old)
        self.new = Rights(new)
