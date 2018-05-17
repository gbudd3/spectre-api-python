import pytest
import spectreapi
import ipaddress

def test_collector(server):
    collector = server.getCollectors()[0]
    assert collector.name == 'RodSerling', "Collectors should have names"

def test_getTargets(server):
    collector = server.getCollectors()[0]
    targets = collector.get_target_cidrs()
    assert ipaddress.ip_network('10.201.0.7') in targets, "10.207.0.7/32 should be in RodSerling targets"

def test_addTargetsAppend(server):
    collector = server.getCollectors()[0]
    collector.set_target_cidrs(ipaddress.ip_network('10.0.0.1'),append=True)
    collector.set_target_cidrs(ipaddress.ip_network('10.0.0.2'),append=True)
    targets = collector.get_target_cidrs()
    assert ipaddress.ip_network('10.0.0.1') in targets, "10.0.0.1/32 should be in RodSerling targets"
    assert ipaddress.ip_network('10.0.0.2') in targets, "10.0.0.2/32 should be in RodSerling targets"

def test_addTargetsOverwrite(server):
    collector = server.getCollectors()[0]
    collector.set_target_cidrs(ipaddress.ip_network('10.201.0.7'))
    targets = collector.get_target_cidrs()
    assert ipaddress.ip_network('10.0.0.1') not in targets, "10.201.0.7/32 should not be in RodSerling targets"

def test_invalid_cidr_type(server):
    collector = server.getCollectorByName('RodSerling')
    try:
        collector._get_cidrs('foo')
    except spectreapi.InvalidArgument:
        assert True, "_get_cidrs('foo') raised an InvalidArgument"
        return
    assert False, "_get_cidrs('foo') should have raised an InvalidArgument"
    

