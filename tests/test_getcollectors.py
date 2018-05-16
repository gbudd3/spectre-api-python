import pytest
import spectreapi

def test_get_collector_by_name(server):

    collector = server.getCollectorByName('RodSerling')
    assert collector.id == 1, "There should be a collector by this name"

