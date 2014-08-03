from jsonable import JSONable

from .unavailable import Unavailable


class User(JSONable):
    __slots__ = ('id', 'text')
    def initialize(self, id, text):
        self.id = self.id = Unavailable.otherwise(id, int)
        self.text = str(text)
