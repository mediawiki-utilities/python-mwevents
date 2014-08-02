from .event import Event, Match


class PageCreated(Event):
    MATCHES = [Match(None, None, True, "new")]
    PRIORITY = 50 # Must be lower than RevisionSaved.PRIORITY
    __slots__ = ('page',)
    def __init__(self, timestamp, user, comment, page):
        super().__init__(timestamp, user, comment)
        self.page = Page(page)
    

# Event.register(PageCreated)
# TODO: Uncomment when ready
