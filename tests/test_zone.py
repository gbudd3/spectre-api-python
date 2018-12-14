'''Double check that get_zones works'''

def test_getzones(server):
    '''Double check that get_zones works'''
    zones = server.get_zones()
    zone = zones[0]
    assert zone.name is not None, "Zones should have names"

def test_create_zone(server):
    '''Validate that create_zone works'''
    zone = server.get_or_create_zone('Test Create Zone')
    assert zone.name is not None, "create_zone didn't work"

def test_create_zone_collector(server):
    '''Validate that create_zone works'''
    zone = server.get_or_create_zone('Test Create Zone')
    collector = zone.get_or_create_collector('Test Create Zone Collector')
    assert collector.name is not None, "get_or_create_collector didn't work"
