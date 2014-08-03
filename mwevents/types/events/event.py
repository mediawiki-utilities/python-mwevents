import copy
from collections import defaultdict

from mw import Timestamp

from jsonable import JSONable

from .. import User
from ... import configuration
from .match import Match


class Event(JSONable):
    __slots__ = ('timestamp', 'user', 'comment')
    MATCHES = NotImplemented
    EVENTS = {}
    MATCH_GROUPS = defaultdict(lambda: [])
    PRIORITY = 99
    
    def initialize(self, timestamp, user, comment):
        self.timestamp = Timestamp(timestamp)
        self.user = User(user)
        self.comment = str(comment)
    
    def to_json(self):
        doc = super().to_json()
        doc['event'] = self.__class__.__name__
        return doc
    
    
    @classmethod
    def from_json(cls, doc):
        if 'event' in doc:
            EventClass = cls.EVENTS.get(doc['event'], cls)
            new_doc = copy.copy(doc)
            del new_doc['event']
            return EventClass.from_json(new_doc)
        else:
            return cls._from_json(doc)
    
    @classmethod
    def register(cls, EventClass):
        for match in EventClass.MATCHES:
            cls.MATCH_GROUPS[match].append(EventClass)
            cls.MATCH_GROUPS[match].sort(key=lambda e:e.PRIORITY)
        
        cls.EVENTS[EventClass.__name__] = EventClass
    
    @classmethod
    def matches(cls, match):
        return cls.MATCH_GROUPS[match]
    
    @classmethod
    def from_rc_doc(cls, rc_doc, config=configuration.DEFAULT):
        match = Match.from_rc_doc(rc_doc)
        
        for EventClass in cls.matches(match):
            yield EventClass.from_rc_doc(rc_doc, config)
        
    @classmethod
    def from_rev_doc(cls, rev_doc, config=configuration.DEFAULT):
        match = Match.from_rev_doc(rev_doc)
        
        for EventClass in cls.matches(match):
            yield EventClass.from_rev_doc(rev_doc, config)
        
    
    @classmethod
    def from_log_row(cls, log_row, config=configuration.DEFAULT):
        match = Match.from_log_row(log_row)
        
        for EventClass in cls.matches(match):
            yield EventClass.from_log_row(log_row, config)
        
    @classmethod
    def from_rc_row(cls, rc_row, config=configuration.DEFAULT):
        match = Match.from_rc_row(rc_row)
        
        for EventClass in cls.matches(match):
            yield EventClass.from_rc_row(rc_doc, config)
