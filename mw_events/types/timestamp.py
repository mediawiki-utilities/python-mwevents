import mw


class Timestamp(mw.Timestamp): #Implements JSONable interface
    
    def to_json(self):
        return self.short_format()
    
    @classmethod
    def from_json(cls, short_format):
        return cls(short_format)
