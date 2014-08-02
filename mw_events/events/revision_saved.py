from .. import configuration
from ..types import Revision
from .event import Event, Match


class RevisionSaved(Event):
    MATCHES = [Match(None, None, True, "edit"),
               Match(None, None, True, "new")]
    __slots__ = ('revision',)
    def initialize(self, timestamp, user, comment, revision):
        super().initialize(timestamp, user, comment)
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

Event.register(RevisionSaved)
