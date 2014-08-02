from collections import defaultdict

from mw import Timestamp

from jsonable import JSONable

from ..types import User


class Event(JSONable):
    __slots__ = ('timestamp', 'user', 'comment')
    MATCHES = NotImplemented
    EVENTS = defaultdict(lambda: [])
    PRIORITY = 99
    
    def initialize(self, timestamp, user, comment):
        self.timestamp = Timestamp(timestamp)
        self.user = User(user)
        self.comment = str(comment)
    
    @classmethod
    def register(cls, EventClass):
        for match in EventClass.MATCHES:
            cls.EVENTS[match].append(EventClass)
            cls.EVENTS[match].sort(key=lambda e:e.PRIORITY)
    
    @classmethod
    def matches(cls, match):
        return cls.EVENTS[match]
    
    @classmethod
    def from_api_doc(cls, api_doc):
        match = Match.from_api_doc(api_doc)
        
        for EventClass in cls.matches(match):
            yield EventClass.from_api_doc(api_doc)
        
    @classmethod
    def from_db_row(cls, db_row):
        match = Match.from_db_row(db_row)
        
        for EventClass in cls.matches(match):
            yield EventClass.from_db_row(api_doc)
