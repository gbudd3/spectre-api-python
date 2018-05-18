import pytest
import spectreapi

def test_get_collector_by_name(server):

    collector = server.get_collector_by_name('RodSerling')
    assert collector.id_num > 0, "There should be a collector by this name"

