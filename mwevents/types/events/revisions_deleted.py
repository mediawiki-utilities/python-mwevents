from ... import configuration
from .event import Event
from .match import Match


class RevisionsDeleted(Event):
    MATCHES = [Match("delete", "revision", True, "log")]
    __slots__ = ('revision',)
    def initialize(self, timestamp, user, comment, rev_ids):
        super().initialize(timestamp, user, comment)
        self.revisions = \
                Unavailable.otherwise(rev_ids, lambda ids:[int(i) for i in ids])
    
    @classmethod
    def from_rc_doc(cls, rc_doc, config=configuration.DEFAULT):
        """
        Example:
            {
                "type": "log",
                "ns": 3,
                "title": "User talk:S205643",
                "pageid": 39719564,
                "revid": 0,
                "old_revid": 0,
                "rcid": 672703228,
                "user": "Mojo Hand",
                "userid": "1453997",
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2014-08-02T17:09:39Z",
                "comment": "[[WP:RD2|RD2]]: Grossly insulting, degrading, or offensive material",
                "logid": 57952428,
                "logtype": "delete",
                "logaction": "revision",
                "0": "revision",
                "1": "619569809",
                "2": "ofield=0",
                "3": "nfield=1",
                "tags": []
            }
        """
        
        if len(rc_doc.get('1', "")) > 0:
            rev_ids = [int(id) for id in rc_doc['1'].split(",")]
        else:
            rev_ids = []
        
        return cls(
            Timestamp(rc_doc['timestamp']),
            User(
                rc_doc.get('userid'),
                rc_doc.get('user')
            ),
            rc_doc.get('comment'),
            rev_ids
        )
        
Event.register(RevisionsDeleted)
