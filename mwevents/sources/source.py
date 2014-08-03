

class Source:
    
    def listen(self, *args, **kwargs):
        raise NotImplementedError()
    
    def query(self, start, end, *args, types=None, **kwargs):
        raise NotImplementedError()
