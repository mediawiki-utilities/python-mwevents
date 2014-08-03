from .. import Unavailable
from ... import configuration
from ...util import split_page_name
from .event import Event
from .match import Match


class UserGroupsModified(Event):
    MATCHES = [Match('rights', 'rights', False, "log")]
    __slots__ = ('modified', 'old', 'new')
    def initialize(self, timestamp, user, comment, modified, old, new):
        super().initialize(timestamp, user, comment)
        
        self.modified = User(modified)
        self.old = [str(group) for group in old]
        self.new = [str(group) for group in new]
    
    @classmethod
    def from_rc_doc(cls, rc_doc, config=configuration.DEFAULT):
        """
        Example:
            {
                "type": "log",
                "ns": 2,
                "title": "User:1980na",
                "pageid": 43436336,
                "revid": 0,
                "old_revid": 0,
                "rcid": 672700514,
                "user": "Pharos",
                "userid": "111996",
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2014-08-02T16:52:37Z",
                "comment": "[[Wikipedia:Education noticeboard#Request for course instructor right: Ninafundisha (talk) (course page draft)]]",
                "logid": 57952057,
                "logtype": "rights",
                "logaction": "rights",
                "rights": {
                    "new": "epinstructor",
                    "old": ""
                },
                "tags": []
            }
        """
        nsname, modified_name = split_page_name(rc_doc['ns'], rc_doc['title'])
        
        if len(rc_doc['rights']['old']) > 0:
            old_groups = rc_doc['rights']['old'].split(",")
        else:
            old_groups = []
        
        if len(rc_doc['rights']['new']) > 0:
            new_groups = rc_doc['rights']['new'].split(",")
        else:
            new_groups = []
        
        
        return cls(
            Timestamp(rc_doc['timestamp']),
            User(
                rc_doc.get('userid'),
                rc_doc.get('user')
            ),
            rc_doc.get('comment'),
            User(
                Unavailable,
                modified_name
            ),
            old_groups,
            new_groups
        )
