import pytest
import spectreapi
import ipaddress

@pytest.fixture()
def server():
    return spectreapi.UsernameServer('6hour', 'admin','admin')

def test_collector(server):
    collector = server.getCollectors()[0]
    assert collector.name == 'RodSerling', "Collectors should have names"

def test_getTargets(server):
    collector = server.getCollectors()[0]
    targets = collector.getTargetCidrs()
    assert ipaddress.ip_network('10.201.0.7') in targets, "10.207.0.7/32 should be in RodSerling targets"

def test_addTargetsAppend(server):
    collector = server.getCollectors()[0]
    collector.setTargetCidrs(ipaddress.ip_network('10.0.0.1'),append=True)
    targets = collector.getTargetCidrs()
    assert ipaddress.ip_network('10.0.0.1') in targets, "10.0.0.1/32 should be in RodSerling targets"

def test_addTargetsOverwrite(server):
    collector = server.getCollectors()[0]
    collector.setTargetCidrs(ipaddress.ip_network('10.201.0.7'))
    targets = collector.getTargetCidrs()
    assert ipaddress.ip_network('10.0.0.1') not in targets, "10.201.0.7/32 should not be in RodSerling targets"

