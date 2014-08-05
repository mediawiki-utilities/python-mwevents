import time

from mw import api

from ..types import StateMarker, Timestamp
from ..types.events import Event, Match


class RCListener:
    
    def __init__(self, session, *, state_marker, events,
                       max_wait, rcs_per_request, stop):
        self.session = session
        
        self.state_marker = state_marker
        self.events = events
        self.max_wait = max_wait
        self.rcs_per_request = rcs_per_request
        self.stop = stop
        self.kwargs = {
            'limit': rcs_per_request,
            'properties': API.RC_EVENT_PROPS,
            'direction': "newer",
            'start': self.state_marker.last_event
        }
        
        if self.events is None:
            self.kwargs['type'] = set(m.rc_type \
                                      for m in Event.MATCH_GROUPS.keys())
        else:
            self.kwargs['type'] = set(m.rc_type \
                                      for e in self.events
                                      for m in e.MATCHES)
        
    
    def __iter__(self):
        while not self.stop():
            start = time.time()
            
            rc_docs, self.kwargs['rccontinue'] = \
                    self.session.recent_changes._query(**self.kwargs)
            
            for rc_doc in rc_docs:
                if self.state_marker.is_after(Timestamp(rc_doc['timestamp']),
                                              rc_doc.get('rcid'),
                                              rc_doc.get('revid'),
                                              rc_doc.get('logid')):
                    
                    for event in Event.from_rc_doc(rc_doc):
                        if self.events is None or type(event) in self.events:
                            yield event
                    
                    self.state_marker.update(Timestamp(rc_doc['timestamp']),
                                             rc_doc.get('rcid'),
                                             rc_doc.get('revid'),
                                             rc_doc.get('logid'))
                
            
            if len(rc_docs) < self.rcs_per_request:
                time.sleep(self.max_wait - (time.time() - start))
    

class API:
    """
    Constructs a source of :class:`mwevents.Event` that connects to a MediaWiki
    API (api.php).
    """
    RC_EVENT_PROPS = {'user', 'userid', 'comment', 'timestamp', 'title', 'ids',
                      'sizes', 'loginfo', 'sha1'}
    
    def __init__(self, session):
        self.session = session
    
    def listener(self, state_marker=None, events=None, max_wait=5,
                       rcs_per_request=100, direction="newer",
                       properties=RC_EVENT_PROPS, stop=lambda: False):
        """
        :Example:
            
            .. code-block:: python
            
                from mwevents.sources import API
                from mwevents import RevisionSaved, PageCreated
                
                api_source = \
                        API.from_api_url("http://en.wikipedia.org/w/api.php")
                
                listener = \
                        api_source.listener(events={RevisionSaved, PageCreated})
                
                for event in listener:
                    if isinstance(event, RevisionSaved):
                        print(event.revision)
                    else: # isinstance(event, PageCreated):
                        print(event.page)
        """
        state_marker = StateMarker(state_marker) \
                       if state_marker is not None \
                       else self._get_current_state()
        
        events = set(events) if events is not None else None
                      
        max_wait = float(max_wait)
        rcs_per_request = int(rcs_per_request)
        
        if not callable(stop):
            raise TypeError("'stop' must be a callable function")
        
        return RCListener(self.session,
                          state_marker=state_marker,
                          events=events,
                          max_wait=max_wait,
                          rcs_per_request=rcs_per_request,
                          stop=stop)
            
    def _get_current_state(self):
        docs = list(self.session.recent_changes.query(properties={'ids',
                                                                  'timestamp'},
                                                      limit=1))
        
        if len(docs) > 0:
            return StateMarker(Timestamp(docs[0]['timestamp']), docs[0]['rcid'])
        else:
            return StateMarker()
        
    def query(self, *args, **kwargs): raise NotImplementedError()
    
    @classmethod
    def from_api_url(cls, url):
        return cls(api.Session(url))
