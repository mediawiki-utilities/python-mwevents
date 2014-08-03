from jsonable import instance


class Match:
    
    RC_TYPES = {
        0: "edit",
        1: "new",
        2: "move",
        3: "log",
        4: "move_over_redirect",
        5: "external"
    }
    
    def __init__(self, type, action, has_rev_id, rc_type):
        self.type       = str(type)
        self.action     = str(action)
        self.has_rev_id = bool(has_rev_id)
        self.rc_type    = str(rc_type)
    
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
        return hash((self.type, self.action, self.has_rev_id, self.rc_type))
    
    def __repr__(self):
        return instance.simple_repr(self.__class__.__name__,
                                    self.type,
                                    self.action,
                                    self.has_rev_id,
                                    self.rc_type)
    
    @classmethod
    def from_rc_doc(cls, rc_doc):
        
        return cls(
            rc_doc.get('logtype'),
            rc_doc.get('logaction'),
            rc_doc.get('revid', 0) > 0,
            rc_doc['type']
        )
    
    @classmethod
    def from_rev_doc(cls, rev_doc):
        
        return cls(
            None,
            None,
            rev_doc.get('revid', 0) > 0,
            "edit" if rev_doc['parentid'] > 0 else "new"
        )
    
    
    @classmethod
    def from_log_row(cls, log_row):
        return cls(
            log_row.get('log_type'),
            log_row.get('log_action'),
            False,
            "log"
        )
        
    @classmethod
    def from_rc_row(cls, rc_row):
        return cls(
            db_row.get('rc_log_type'),
            db_row.get('rc_log_action'),
            rc_doc.get('rc_this_oldid', 0) > 0,
            cls.RC_TYPES[db_row['rc_type']]
        )
