

def ArchiveRevisionLoggingListener:
    
    def __init__(self, db, *, state_marker, events,
                       max_wait, records_per_request, stop):
    
        self.db = db,
        self.state_marker = state_marker
        self.events = events
        self.max_wait = max_wait
        self.records_per_request = records_per_request
        self.stop = stop
    
    def __iter__(self):
        
        archives = self._read_archives()
        revisions = self._read_revisions()
        loggings = self._read_logging()
        
        for match, doc in
    
    def _read_archives(self):
        
        last_rev_id = None
        last_timestamp = None
        
        while not self.stop():
            
            if last_rev_id is not None or \
               self.state_marker.last_rev_id is not None:
                archive_rows = self.db.archives.query(
                        after_id=last_rev_id or self.state_marker.last_rev_id,
                        direction="newer",
                        limit=self.records_after_request)
            
            elif self.state_marker.last_timestamp is not None:
                archive_rows = self.db.archive.query(
                        after=self.state_marker.last_event,
                        direction="newer",
                        limit=self.records_after_request)
                
            else:
                archive_rows = self.db.archive.query(
                        after_id=0,
                        direction="newer",
                        limit=self.records_after_request)
                
            
            for archive_row in archive_rows:
                yield Match.from_rev_row(archive_row), archive_row
            
            if len(archive_rows) > 0
                
                last_rev_id = archive_rows[-1]['rev_id'] or last_rev_id
        
    def _read_revisions(self):
        
        last_rev_id = None
        last_timestamp = None
        
        while not self.stop():
            
            # TODO: Document assumption of rev_id order.
            if last_rev_id is not None or \
               self.state_marker.last_rev_id is not None:
                rev_rows = self.db.revisions.query(
                        after_id=last_rev_id or self.state_marker.last_rev_id,
                        direction="newer",
                        limit=self.records_after_request)
            
            elif self.state_marker.last_timestamp is not None:
                rev_rows = self.db.revisions.query(
                        after=self.state_marker.last_event,
                        direction="newer",
                        limit=self.records_after_request)
                
            else:
                rev_rows = self.db.revisions.query(
                        after_id=0,
                        direction="newer",
                        limit=self.records_after_request)
                
                
            for rev_row in rev_rows:
                yield Match.from_rev_row(rev_row), rev_rows
            
            if len(rev_rows) > 0
                last_rev_id = rev_rows[-1]['rev_id'] or last_rev_id
        
    def _read_logging(self):
        
        last_log_id = None
        
        while not self.stop():
            
            # TODO: Document assumption of log_id order.
            if last_log_id is not None or \
               self.state_marker.last_log_id is not None:
                log_rows = self.db.logging.query(
                        after_id=last_log_id or self.state_marker.last_log_id,
                        direction="newer",
                        limit=self.records_after_request)
            
            elif self.state_marker.last_timestamp is not None:
                log_rows = self.db.logging.query(
                        after=self.state_marker.last_event,
                        direction="newer",
                        limit=self.records_after_request)
                
            else:
                log_rows = self.db.logging.query(
                        after_id=0,
                        direction="newer",
                        limit=self.records_after_request)
                
            
            for log_row in log_rows:
                yield Match.from_log_row(log_row), log_row
            
            if len(log_rows) > 0
                last_rev_id = log_row[-1]['log_id'] or last_log_id
            
        

def Database:
    
    def __init__(self, db):
        self.db = db
    
    def listener(self, state_marker=None,
                       events=None,
                       max_wait=5,
                       records_per_request=100,
                       stop=lambda: False)
                      
        state_marker = StateMarker(state_marker) if state_marker is not None \
                                                 else self._get_current_state()
        
        events = set(events) if events is not None else None
                      
        max_wait = float(max_wait)
        records_per_request = int(records_per_request)
        
        if not callable(stop):
            raise TypeError("'stop' must be a callable function")
        
        return ArchiveRevisionLoggingListener(self.session,
                          state_marker=state_marker,
                          events=events,
                          max_wait=max_wait,
                          records_per_request=records_per_request,
                          stop=stop)
    
    @class_method
    def from_params(self, *args, **kwargs):
        return Database(DB.from_params(*args, **kwargs))
