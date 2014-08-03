from nose.tools import eq_

from ..state_marker import StateMarker
from ..timestamp import Timestamp


def test_construction_and_values():
    last_event = Timestamp(1234567890)
    last_rc_id = 10
    last_rev_id = 8
    last_log_id = None
    
    state_maker = StateMarker(last_event, last_rc_id, last_rev_id, last_log_id)
    
    eq_(state_maker.last_event, last_event)
    eq_(state_maker.last_rc_id, last_rc_id)
    eq_(state_maker.last_rev_id, last_rev_id)
    eq_(state_maker.last_log_id, last_log_id)
    
    eq_(state_maker, StateMarker(state_maker))
    eq_(state_maker, StateMarker(state_maker.to_json()))

def test_is_after():
    last_event = Timestamp(1234567890)
    last_rc_id = 10
    last_rev_id = 8
    last_log_id = None
    
    state_maker = StateMarker(last_event, last_rc_id, last_rev_id, last_log_id)
    
    assert not state_maker.is_after(last_event,
                                    last_rc_id,
                                    last_rev_id,
                                    last_log_id)
    
    assert state_maker.is_after(last_event+1,
                                last_rc_id,
                                last_rev_id,
                                last_log_id)
    
    assert state_maker.is_after(last_event,
                                last_rc_id+1,
                                last_rev_id,
                                last_log_id)
    
    assert state_maker.is_after(last_event,
                                last_rc_id,
                                last_rev_id+1,
                                last_log_id)
    
    assert state_maker.is_after(last_event,
                                last_rc_id,
                                last_rev_id,
                                1)
    
    assert not state_maker.is_after(last_event-1,
                                    None,
                                    last_rev_id+1,
                                    None)
