MediaWiki events
================
Wiki-tool builders & researchers rely on various sources of information about what's happened and is currently happening in Wikipedia. These data sources tend to be structured in differently and contain incomplete or poorly structured information.  Some datasources are queryable, but require complexity to "listen" to ongoing events while others are intended to only be used to "listen" to current events. ''MediaWiki events'' is designed to minimize the frustration involved in process MediaWiki's events.


**Instal with pip:** ``pip install mwevents``

**Note:** *Use of this library requires Python 3 or later.*

**Documentation:** *Comming soon!*

:Example:

    .. code-block:: python

        from mwevents.sources import API
        from mwevents import RevisionSaved, PageCreated
        
        api_source = API.from_api_url("http://en.wikipedia.org/w/api.php")
        listener = api_source.listener(events={RevisionSaved, PageCreated})
        
        for event in listener:
            if isinstance(event, RevisionSaved):
                print(event.revision)
            else: # isinstance(event, PageCreated):
                print(event.page)

About the author
================
:name:
	Aaron Halfaker
:email:
	aaron.halfaker@gmail.com
:website:
	http://halfaker.info --
	http://en.wikipedia.org/wiki/User:EpochFail

Contributors
============
None yet.  See http://github.com/halfak/MediaWiki-events.  Pull requests are encouraged.
