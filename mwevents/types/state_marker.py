
from jsonable import JSONable

from .timestamp import Timestamp


class StateMarker(JSONable):
    __slots__ = ("last_event", "last_rev_id", "last_rc_id", "last_log_id")
    def initialize(self, last_event=None, last_rc_id=None,
                         last_rev_id=None, last_log_id=None):
        self.last_event = Timestamp(last_event) \
                          if last_event is not None else None
        self.last_rc_id = int(last_rc_id) \
                          if last_rc_id is not None else None
        self.last_rev_id = int(last_rev_id) \
                          if last_rev_id is not None else None
        self.last_log_id = int(last_log_id) \
                          if last_log_id is not None else None
        
    def update(self, timestamp, rc_id, rev_id, log_id):
        self.last_event = timestamp or self.last_event
        self.last_rc_id = rc_id or self.last_rc_id
        self.last_rev_id = rev_id or self.last_rev_id
        self.last_log_id = log_id or self.last_log_id
        
    def is_after(self, timestamp, rc_id, rev_id, log_id):
        timestamp = Timestamp(timestamp)
        
        return (self.last_event is not None and
                timestamp > self.last_event) or\
               (
                   (self.last_event is None or
                    timestamp == self.last_event) and
                   (
                       (rc_id is not None and
                        rc_id > (self.last_rc_id or 0)) or\
                       (rev_id is not None and
                        rev_id > (self.last_rev_id or 0)) or\
                       (log_id is not None and
                        log_id > (self.last_log_id or 0))
                    )
                )
