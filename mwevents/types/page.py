from jsonable import JSONable

from .unavailable import Unavailable


class Page(JSONable):
    __slots__ = ('id', 'namespace', 'title')
    def initialize(self, id, namespace, title):
        self.id = Unavailable.otherwise(id, int)
        self.namespace = int(namespace)
        self.title = str(title)
