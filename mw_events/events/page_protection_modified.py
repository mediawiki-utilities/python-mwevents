from .event import Event, Match


class PageProtectionModified(Event):
    MATCHES = [Match("protect", "protect", False, "log"),
               Match("protect", "modify", False, "log"),
               Match("protect", "unprotect", False, "log")]
    __slots__ = ('page', 'action', 'protection')
    def __init__(self, timestamp, user, comment, page, action, protection):
        super().__init__(timestamp, user, comment)
        self.page = Page(page)
        self.action = str(action)
        self.protection = Protection(protection)
    
# Event.register(PageProtectionModified)
# TODO: Uncomment when ready
