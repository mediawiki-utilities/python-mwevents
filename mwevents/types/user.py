from jsonable import JSONable


class User(JSONable):
    __slots__ = ('id', 'text')
    def initialize(self, id, text):
        self.id = int(id) if id is not None else None
        self.text = str(text)
