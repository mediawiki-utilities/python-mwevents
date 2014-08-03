import time

from mw import api

from ..types import StateMarker, Timestamp
from ..types.events import Event, Match


class RCListener:
    
    def __init__(self, session, *, state_marker, events,
                       min_wait, rcs_per_request, stop):
        self.session = session
        
        self.state_marker = state_marker
        self.events = events
        self.min_wait = min_wait
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
                time.sleep(min_wait - (time.time() - start))
    

class API:
    """
    Constructs a source of :class:`mwevents.Event` that connects to a MediaWiki
    API (api.php).
    """
    RC_EVENT_PROPS = {'user', 'userid', 'comment', 'timestamp', 'title', 'ids',
                      'sizes', 'loginfo', 'sha1'}
    
    def __init__(self, session):
        self.session = session
    
    def listener(self, state_marker=None, events=None, min_wait=5,
                       rcs_per_request=100, direction="newer",
                       properties=RC_EVENT_PROPS, stop=lambda: False):
       """
       :Example:
           
           .. code-block:: python
           
               import sys

               from mwevents.sources import API
               from mwevents import RevisionSaved, PageCreated

               API_URL = "http://en.wikipedia.org/w/api.php"
               try:
                   api_source = API.from_api_url(API_URL)
                   listener = api_source.listener(events={RevisionSaved,
                                                          PageCreated})
                   for event in listener:
                       if isinstance(event, RevisionSaved):
                           print("Revision {0} of {1} saved by {2}."\
                                 .format(event.revision.id,
                                         event.revision.page_id,
                                         event.user))
                       else: # isinstance(event, PageCreated):
                           print("Page {0}:{1} created by {2}."\
                                 .format(event.page.namespace,
                                         event.page.title,
                                         event.user))
                   
               except KeyboardInterrupt:
                   sys.stderr.write("Keyboard Interrupt caught.  " + \
                                    "Shutting down.\n")
                   sys.stderr.write(str(listener.state_marker.to_json()) + "\n")
       """
            state_marker = StateMarker(state_marker) \
                                if state_marker is not None else StateMarker()
            
            events = set(events) if events is not None else None
                          
            min_wait = float(min_wait)
            rcs_per_request = int(rcs_per_request)
            
            if not callable(stop):
                raise TypeError("'stop' must be a callable function")
            
            return RCListener(self.session,
                              state_marker=state_marker,
                              events=events,
                              min_wait=min_wait,
                              rcs_per_request=rcs_per_request,
                              stop=stop)
            
        
    def query(self, *args, **kwargs): raise NotImplemented Error
    
    @classmethod
    def from_api_url(cls, url):
        return cls(api.Session(url))
