from .. import Page, Protection, Timestamp, Unavailable, User
from ... import configuration
from ...util import split_page_name
from .event import Event
from .match import Match


class PageProtectionModified(Event):
    MATCHES = [Match("protect", "protect", False, "log"),
               Match("protect", "modify", False, "log"),
               Match("protect", "unprotect", False, "log")]
    __slots__ = ('page', 'action', 'protections')
    def initialize(self, timestamp, user, comment, page, action, protections):
        super().initialize(timestamp, user, comment)
        self.page = Page(page)
        self.action = Unavailable.otherwise(action, str, none_ok=False)
        self.protections = \
            Unavailable.otherwise(protections,
                                  lambda ps: [Protection(p) for p in ps])
        
    @classmethod
    def from_rc_doc(cls, rc_doc, config=configuration.DEFAULT):
        """
        Example:
            {
                "type": "log",
                "ns": 0,
                "title": "Alice (Avril Lavigne song)",
                "rcid": 616736350,
                "pageid": 25727375,
                "revid": 0,
                "old_revid": 0,
                "user": "Mark Arsten",
                "userid": "15020596",
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2013-11-14T03:20:35Z",
                "comment": "Persistent IP edit warring",
                "logid": 52608670,
                "logtype": "protect",
                "logaction": "protect",
                "0": "\u200e[edit=autoconfirmed] (expires 03:20, 21 November 2013 (UTC))",
                "1": "",
                "tags": []
            }
            {
                "type": "log",
                "ns": 4,
                "title": "Wikipedia:Requests for page protection",
                "pageid": 352651,
                "revid": 0,
                "old_revid": 0,
                "rcid": 672604441,
                "user": "NativeForeigner",
                "userid": "964805",
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2014-08-02T05:51:34Z",
                "comment": "Persistent [[WP:Vandalism|vandalism]]/[[WP:BLP|BLP Issues]]",
                "logid": 57939003,
                "logtype": "protect",
                "logaction": "modify",
                "0": "\u200e[edit=autoconfirmed] (expires 00:00, 31 August 2014 (UTC))\u200e[move=sysop] (indefinite)",
                "1": "",
                "tags": []
            }
            {
                "type": "log",
                "ns": 6,
                "title": "File:ElmerFlick.jpg",
                "rcid": 616706496,
                "pageid": 986245,
                "revid": 0,
                "old_revid": 0,
                "user": "DYKUpdateBot",
                "userid": "11745509",
                "bot": "",
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2013-11-14T00:05:14Z",
                "comment": "File off the [[T:DYK|DYK]] section of the Main Page",
                "logid": 52605770,
                "logtype": "protect",
                "logaction": "unprotect",
                "tags": []
            }
        """
        nsname, title = split_page_name(rc_doc['ns'], rc_doc['title'])
        
        if rc_doc['logaction'] in ("protect", "modify"):
            protections = Protection.from_params(
                                rc_doc.get('0', ""),
                                expiration_format=config['expiration_format'],
                                indefinite=config['indefinite'])
            
        elif rc_doc['logaction'] == "unprotect":
            protections = []
            
        else:
            assert False, "Shouldn't happen."
        
        return cls(
            Timestamp(rc_doc['timestamp']),
            User(
                rc_doc.get('userid'),
                rc_doc.get('user')
            ),
            rc_doc.get('comment'),
            Page(
                rc_doc.get('pageid'),
                rc_doc.get('ns'),
                title
            ),
            rc_doc['logaction'],
            protections
        )
    
Event.register(PageProtectionModified)
