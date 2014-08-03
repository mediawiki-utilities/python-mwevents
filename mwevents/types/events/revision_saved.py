from .. import Revision, Timestamp, Unavailable, User
from ... import configuration
from .event import Event
from .match import Match


class RevisionSaved(Event):
    __slots__ = ('revision',)
    MATCHES = [Match(None, None, True, "edit"),
               Match(None, None, True, "new")]
    def initialize(self, timestamp, user, comment, revision):
        super().initialize(timestamp, user, comment)
        self.revision = Revision(revision)
    
    @classmethod
    def from_rc_doc(cls, rc_doc, config=configuration.DEFAULT):
        """
        Example:
            {
                "type": "edit",
                "ns": 1,
                "title": "Talk:Neutral mutation",
                "rcid": 616266829,
                "pageid": 5555386,
                "revid": 581269873,
                "old_revid": 581268750,
                "user": "Grabriggs",
                "userid": "19701352",
                "oldlen": 23767,
                "newlen": 24046,
                "timestamp": "2013-11-12T01:48:22Z",
                "comment": "/* Neutral theory */",
                "tags": [],
                "sha1": "8817b4efd42c936254dfb09ce5bbfd0e4f9b848a"
            }
        """
        
        return cls(
            Timestamp(rc_doc['timestamp']),
            User(
                rc_doc.get('userid'),
                rc_doc.get('user')
            ),
            rc_doc.get('comment'),
            Revision(
                rc_doc.get('revid'),
                rc_doc.get('old_revid'),
                rc_doc.get('newlen'),
                rc_doc.get('sha1'),
                rc_doc.get('pageid'),
                'minor' in rc_doc
            )
        )
    
    @classmethod
    def from_rev_doc(cls, rev_doc, config=configuration.DEFAULT):
        """
        Example:
            {
                "revid": 619093743,
                "parentid": 618899706,
                "user": "Eduen",
                "userid": 7527773,
                "timestamp": "2014-07-30T07:26:05Z",
                "size": 181115,
                "sha1": "c6236e5ad7b6af7c353a43ded631298c2b7e95ea",
                "contentmodel": "wikitext",
                "comment": "another quote from a prominent anarchist theroy which talks againts the simplification of a libertarian society to simply the absence of a state",
                "page": {
                    "pageid": 12,
                    "ns": 0,
                    "title": "Anarchism"
                }
            }
        """
        return cls(
            Timestamp(rev_doc['timestamp']),
            User(
                rev_doc.get('userid'),
                rev_doc.get('user')
            ),
            rev_doc.get('comment'),
            Revision(
                rev_doc['revid'],
                rev_doc['parentid'],
                rev_doc['size'],
                rev_doc['sha1'],
                rev_doc['page']['pageid'],
                "minor" in rev_doc
            )
        )
    
    @classmethod
    def from_rev_row(cls, rev_row, config=configuration.DEFAULT):
        """
        Example:
            {
                'rev_id': 233192,
                'rev_page': 10,
                'rev_text_id': 233192,
                'rev_comment': "*",
                'rev_user': 99,
                'rev_user_text': "RoseParks",
                'rev_timestamp': "20010121021221",
                'rev_minor_edit': 0,
                'rev_deleted': 0,
                'rev_len': 124,
                'rev_parent_id': 0,
                'rev_sha1': "8kul9tlwjm9oxgvqzbwuegt9b2830vw"
            }
        """
        return cls(
            Timestamp(rev_row['rev_timestamp']),
            User(
                rev_row['rev_user'],
                rev_row['rev_user_text']
            ),
            rev_row['rev_comment'],
            Revision(
                rev_row['rev_id'],
                rev_row['rev_parent_id'],
                rev_row['rev_len'],
                rev_row['rev_sha1'],
                rev_row['rev_page'],
                rev_row['rev_minor_edit']
            )
        )
    
    @classmethod
    def from_rc_row(cls, rc_row, config=configuration.DEFAULT):
        """
        Example:
            {
                rc_id: 624362534
                rc_timestamp: "20131219020516"
                rc_cur_time: ""
                rc_user: 16380370
                rc_user_text: "RedVanderwall"
                rc_namespace: 0
                rc_title: "Narragansett_Race_Track"
                rc_comment: "/* The Biscuit */"
                rc_minor: 1
                rc_bot: 0
                rc_new: 0
                rc_cur_id: 10680758
                rc_this_oldid: 586726430
                rc_last_oldid: 586725822
                rc_type: 0
                rc_source: mw.edit
                rc_moved_to_ns: 0
                rc_moved_to_title: ""
                rc_patrolled: 0
                rc_ip: <redacted>
                rc_old_len: 24309
                rc_new_len: 24348
                rc_deleted: 0
                rc_logid: 0
                rc_log_type: NULL
                rc_log_action: ""
                rc_params:
            }
        """
        return cls(
            Timestamp(rc_row['rc_timestamp']),
            User(
                rc_row['rc_user'],
                rc_row['rc_user_text']
            ),
            rc_row['rc_comment'],
            Revision(
                rc_row['rc_this_oldid'],
                rc_row['rc_last_oldid'],
                rc_row['rc_new_len'],
                rc_row['rev_sha1'] if 'rev_sha1' in rc_row else Unavailable,
                rc_row['rc_cur_id'],
                rc_row['rc_minor']
            )
        )
    
Event.register(RevisionSaved)
