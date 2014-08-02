from .event import Event, Match


class PageRestored(Event):
    MATCHES = [Match("delete", "restore", False, "log")]
    __slots__ = ('old_page_id', 'page')
    def __init__(self, timestamp, user, comment, old_page_id, page):
        super().__init__(timestamp, user, comment)
        self.old_page_id = int(old_page_id)
        self.page = Page(page)
    
    @classmethod
    def from_api_doc(cls, api_doc, config=defaults.CONFIG): pass
    

# Event.register(RevisionSaved)
# TODO: Uncomment when ready
