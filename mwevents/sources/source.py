
class RCListener:
    
    def __iter__(self): raise NotImplementedError()


class Source:
    
    def listener(self, *args, **kwargs):
        raise NotImplementedError()
    
    def query(self, start, end, *args, types=None, **kwargs):
        raise NotImplementedError()
