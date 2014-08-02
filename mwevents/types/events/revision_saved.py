from .event import Event, Match


class RevisionSaved(Event):
    MATCHED = [Match(None, None, True, "edit"),
               Match(None, None, True, "new", priority=50)]
    __slots__ = ('revision',)
    def __init__(self, timestamp, user, comment, revision):
        super().__init__(timestamp, user, comment)
        self.revision = Revision(revision)
    
    @classmethod
    def from_api_doc(cls, api_doc, config=configuration.DEFAULTS):
        """
        :Example API doc::
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
        ns, title = config.title_parser.parse(api_doc['title'])
        assert ns == api_doc['ns']
        
        return cls(
            Timestamp(api_doc['timestamp']),
            User(
                int(api_doc['userid']),
                api_doc['user']
            ),
            api_doc['comment'],
            Revision(
                api_doc['revid'],
                api_doc['old_revid'],
                api_doc['newlen'],
                api_doc['sha1'],
                api_doc['pageid'],
                'minor' in api_doc
            )
        )
    
    @classmethod
    def from_rev_row(cls, rev_row):
        return cls(
            Timestamp(db_row['rev_timestamp'])
            User(
                row(db_row['rev_user']),
                row['rev_user_text']
            ),
            rev['rev_comment'],
            Revision(
                db_row['rev_id'],
                db_row['rev_parent_id'],
                db_row['rev_len'],
                db_row['rev_sha1'],
                db_row['rev_page'],
                db_row['rev_minor']
            )
        )
    
    @classmethod
    def from_rc_row(cls, rc_row):
        """
        :Example DB row::
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
        """
        return cls(
            Timestamp(db_row['rc_timestamp'])
            User(
                row(db_row['rc_user']),
                row['rc_user_text']
            ),
            rev['rc_comment'],
            Revision(
                db_row['rc_this_oldid'],
                db_row['rc_last_oldid'],
                db_row['rc_new_len'],
                None, # Not available
                db_row['rc_cur_id'],
                db_row['rc_minor']
            )
        )
    
Event.register(RevisionSaved)
