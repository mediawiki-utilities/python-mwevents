from jsonable import JSONable

from .unavailable import Unavailable


class Revision(JSONable):
    __slots__ = ('id', 'parent_id', 'bytes', 'sha1', 'page_id', 'minor')
    def initialize(self, id, parent_id, bytes, sha1, page_id, minor):
        self.id = Unavailable.otherwise(id, int)
        self.parent_id = Unavailable.otherwise(parent_id, int) or 0
        self.bytes = Unavailable.otherwise(bytes, int)
        self.sha1 = Unavailable.otherwise(sha1, str)
        self.page_id = Unavailable.otherwise(page_id, int)
        self.minor = Unavailable.otherwise(minor, bool)
