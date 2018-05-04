import pytest
import spectreapi

@pytest.fixture()
def server():
    return spectreapi.UsernameServer('6hour', 'admin','admin')

def test_getzones(server):
    zones = server.getZones()
    zone = zones[0]
    assert zone.name is not None, "Zones should have names"
