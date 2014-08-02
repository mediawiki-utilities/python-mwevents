from jsonable import JSONable


class Revision(JSONable):
    __slots__ = ('id', 'parent_id', 'bytes', 'sha1', 'page_id', 'minor')
    def initialize(self, id, parent_id, bytes, sha1, page_id, minor):
        self.id = int(id)
        self.parent_id = int(parent_id) if parent_id is not None else 0
        self.bytes = int(bytes)
        self.sha1 = str(sha1)
        self.page_id = int(page_id)
        self.minor = bool(minor)
