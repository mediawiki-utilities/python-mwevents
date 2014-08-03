import time

from mw import api

from ..types import Event


class API:
    """
    Example:
        
        .. code-block::python
    """
    RC_PROPS = {'user', 'userid', 'comment', 'timestamp', 'title', 'ids',
                'sizes', 'loginfo', 'sha1'}
    
    def __init__(self, session):
        self.session = session
    
    def listen(self, *args, min_wait=5, rcs_per_request=50,
                      stop=lambda: False,
                      direction="newer",
                      properties=RC_PROPS, types=None, **kwargs):
        
        kwargs['limit'] = rcs_per_request
        kwargs['properties'] = properties
        kwargs['direction'] = direction
        
        while not stop():
            start = time.time()
            
            rc_docs, kwargs['rccontinue'] = \
                    self.session.recent_changes._query(*args, **kwargs)
            
            for rc_doc in rc_docs:
                print(rc_doc)
                state = rc_doc['timestamp'] + "|" + str(rc_doc['rcid'])
                for event in Event.from_rc_doc(rc_doc):
                    if types is None or type(event) in types:
                        yield event, state
                
            
            if len(rc_docs) < rcs_per_request:
                time.sleep(min_wait - (time.time() - start))
            
        
    @classmethod
    def from_api_url(cls, url):
        return cls(api.Session(url))
