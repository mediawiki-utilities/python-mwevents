"""
Listens to a wiki's recentchanges feed and prints standardized JSON events.

Usage:
    listen <api_url> [--revisions-only] [--store-state=<path>]

Options:
    <api_url>             The url for the MediaWiki API to connect to.
    --revisions-only      Only print RevisionSaved events.
    --store-state=<path>  A file location to read and store read state to.
"""
import json
import os.path
import pprint
import sys

from docopt import docopt

try:
    sys.path.insert(0, ".")
    from mwevents.sources import API
    from mwevents import RevisionSaved, StateMarker
except:
    raise

def main():
    args = docopt(__doc__)
    
    run(args['<api_url>'], args['--revisions-only'], args['--store-state'])

def run(api_url, revisions_only, store_state):
    api_source = API.from_api_url(api_url)
    
    if revisions_only:
        events = {RevisionSaved}
    else:
        events = None
    
    state_marker = load_state_marker(store_state)
    
    try:
        listener = api_source.listener(state_marker=state_marker, events=events)
        for event in listener:
            
            pprint.pprint(event.to_json())
            
            if store_state is not None:
                with open(store_state, "w") as f:
                    json.dump(listener.state_marker.to_json(), f)
                
            
        
    except KeyboardInterrupt:
        print("Keyboard interrupt received.  Shutting down.")


def load_state_marker(path):
    if path is not None:
        
        if os.path.exists(path):
            try:
                return StateMarker(json.load(open(path)))
            except ValueError:
                pass

if __name__ == "__main__": main()
