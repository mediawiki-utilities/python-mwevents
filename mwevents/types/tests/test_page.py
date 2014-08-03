from nose.tools import eq_

from ..page import Page


def test_construction_and_values():
    id = 129
    namespace = 272
    title = "foobar!"
    
    page = Page(id, namespace, title)
    
    eq_(page.id, id)
    eq_(page.namespace, namespace)
    eq_(page.title, title)
    
    eq_(page, Page(page))
    eq_(page, Page(page.to_json()))
