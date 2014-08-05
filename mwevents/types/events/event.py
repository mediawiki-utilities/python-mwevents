import copy
from collections import defaultdict

from mw import Timestamp

from jsonable import AbstractJSONable, JSONable

from .. import User
from ... import configuration
from .match import Match


class Event(AbstractJSONable):
    __slots__ = ('timestamp', 'user', 'comment')
    MATCHES = NotImplemented
    MATCH_GROUPS = defaultdict(lambda: [])
    PRIORITY = 99
    CLASS_NAME_KEY = "event"
    
    def initialize(self, timestamp, user, comment):
        self.timestamp = Timestamp(timestamp)
        self.user = User(user)
        self.comment = str(comment)
    
    @classmethod
    def register(cls, EventClass):
        for match in EventClass.MATCHES:
            cls.MATCH_GROUPS[match].append(EventClass)
            cls.MATCH_GROUPS[match].sort(key=lambda e:e.PRIORITY)
        
        super().register(EventClass)
    
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
