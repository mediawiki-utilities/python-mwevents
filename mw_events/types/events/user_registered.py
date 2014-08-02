from .event import Event, Match


class UserRegistered(Event):
    MATCHES = [Match("newusers", "newusers", False, "log"),
               Match("newusers", "create", False, "log"),
               Match("newusers", "create2", False, "log"),
               Match("newusers", "autocreate", False, "log"),
               Match("newusers", "byemail", False, "log")]
    __slots__ = ('action', 'newuser')
    def __init__(self, timestamp, user, comment, action, new):
        super().__init__(timestamp, user, comment)
        self.action = str(action)
        self.new = User(new)
        
    @classmethod
    def from_api_doc(cls, api_doc, config=configuration.DEFAULT):
        """
        Example:
            {
                "type": "log",
                "ns": 2,
                "title": "User:IntDebBall",
                "rcid": 616284425,
                "pageid": 0,
                "revid": 0,
                "old_revid": 0,
                "user": "IntDebBall",
                "userid": 20124261,
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2013-11-12T03:56:32Z",
                "comment": "",
                "logid": 52558177,
                "logtype": "newusers",
                "logaction": "create",
                "tags": []
            },
            {
                "type": "log",
                "ns": 2,
                "title": "User:Fredielyn Bucio",
                "rcid": 616279592,
                "pageid": 0,
                "revid": 0,
                "old_revid": 0,
                "user": "Palmville",
                "userid": 20124109,
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2013-11-12T03:19:42Z",
                "comment": "",
                "logid": 52557705,
                "logtype": "newusers",
                "logaction": "create2",
                "tags": []
            },
            {
                "type": "log",
                "ns": 2,
                "title": "User:Phillykidd",
                "rcid": 616286015,
                "pageid": 0,
                "revid": 0,
                "old_revid": 0,
                "user": "Callanecc",
                "userid": 20124315,
                "oldlen": 0,
                "newlen": 0,
                "timestamp": "2013-11-12T04:09:32Z",
                "comment": "Requested account at [[WP:ACC]], request #110880",
                "logid": 52558431,
                "logtype": "newusers",
                "logaction": "byemail",
                "tags": []
            }
        """
        if api_doc['logaction'] == "create":
            user_name = api_doc['user']
            user_id
        else: #doc['logaction'] in ("create2","byemail")
            ns, name_title = config.title_parser.parse(doc['title'])
            assert ns == 2
            user_name = name_title
            user_id = None # Not available
        
        return cls(
            Timestamp(api_doc['timestamp'])
            User(
                api_doc['userid'],
                api_doc['name']
            ),
            api_doc['comment'],
            api_doc['logaction'],
            User(
                user_id,
                user_name
            )
        )
        
    

# Event.register(UserRegistered)
# TODO: Uncomment when ready
