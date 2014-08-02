from collections import defaultdict

from mw import Timestamp


class Event:
    __slots__ = ('timestamp', 'user')
    MATCHES = NotImplemented
    EVENTS = defaultdict(lambda: [])
    
    def __init__(self, timestamp, user, comment):
        self.timestamp = Timestamp(timestamp)
        self.user = User(user)
    
    @classmethod
    def register(cls, EventClass):
        for match in event_class.MATCHES:
            cls.EVENTS[match].append(EventClass)
            cls.EVENTS.sort(key=lambda m:m.priority)
    
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

class Match:
    
    RC_TYPES = {
        0: "edit",
        1: "new",
        2: "move",
        3: "log",
        4: "move_over_redirect",
        5: "external"
    }
    
    def __init__(self, type, action, has_rev_id, rc_type, priority=99):
        self.type       = str(type)
        self.action     = str(action)
        self.has_rev_id = bool(has_rev_id)
        self.rc_type    = str(rc_type)
        self.priority   = int(priority)
    
    def __eq__(self, other):
        try:
            return (
                self.type == other.type and
                self.action == other.action and
                self.has_rev_id == other.has_rev_id and
                self.rc_type    == other.rc_type
            )
        except AttributeError:
            return False
    
    def __hash__(self):
        return hash(self.type, self.action, self.has_rev_id, self.rc_type)
    
    @classmethod
    def from_api_doc(cls, api_doc):
        
        return cls(
            doc.get('logtype'),
            doc.get('logaction'),
            doc.get('revid', 0) > 0,
            doc['type']
        )
            
    
    @classmethod
    def from_db_row(cls, db_row):
        return cls(
            db_row.get('log_type'),
            db_row.get('log_action'),
            'rev_id' in db_row and \
                    db_row['rev_id'] is not None and
                    db_row['rev_id'] > 0,
            cls.RC_TYPES[db_row['rc_type']]
        )
