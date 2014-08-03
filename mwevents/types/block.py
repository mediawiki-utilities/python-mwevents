from jsonable import JSONable

from .timestamp import Timestamp
from .unavailable import Unavailable


class Block(JSONable):
    __slots__ = ('flags', 'duration', 'expiration')
    def initialize(self, flags, duration, expiration):
        self.flags = [str(flag) for flag in flags]
        self.duration = str(duration)
        self.expiration = Unavailable.otherwise(expiration, Timestamp)
