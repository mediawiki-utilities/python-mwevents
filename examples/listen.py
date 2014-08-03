"""
Listens to a wiki's recentchanges feed.

Usage:
    listen <api_url>

Options:
    <api_url>  The url for the MediaWiki API to connect to.
"""
import pprint
import sys

from docopt import docopt

try:
    sys.path.insert(0, ".")
    from mwevents.sources import API
except:
    raise

def main():
    args = docopt(__doc__)
    
    run(args['<api_url>'])

def run(api_url):
    
    api_source = API.from_api_url(api_url)
    
    try:
        for event, state in api_source.listen():
            
            pprint.pprint(event.to_json())
        
    except KeyboardInterrupt:
        print("Keyboard interrupt received.  Shutting down.")


if __name__ == "__main__": main()
