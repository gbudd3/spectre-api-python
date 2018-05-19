'''Double check that get_zones works'''

def test_getzones(server):
    '''Double check that get_zones works'''
    zones = server.get_zones()
    zone = zones[0]
    assert zone.name is not None, "Zones should have names"
