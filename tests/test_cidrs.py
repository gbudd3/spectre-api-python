'''Test the Collector cidr methods '''
import ipaddress
import spectreapi

def test_collector(server):
    '''Make sure we can get collectors'''
    collector = server.get_collector_by_name('RodSerling')
    assert collector.name == 'RodSerling', "Collectors should have names"

def test_get_targets(server):
    '''Make sure we can get targets from that collector'''
    collector = server.get_collector_by_name('RodSerling')
    targets = collector.get_target_cidrs()
    assert ipaddress.ip_network('10.201.0.7') in targets, "CIDR should be in RodSerling targets"

def test_add_targets_append(server):
    '''Add targets to a collector'''
    collector = server.get_collector_by_name('RodSerling')
    collector.set_target_cidrs(ipaddress.ip_network('10.0.0.1'), append=True)
    collector.set_target_cidrs(ipaddress.ip_network('10.0.0.2'), append=True)
    targets = collector.get_target_cidrs()
    assert ipaddress.ip_network('10.0.0.1') in targets, "CIDR should be in RodSerling targets"
    assert ipaddress.ip_network('10.0.0.2') in targets, "CIDR should be in RodSerling targets"

def test_add_targets_overwrite(server):
    '''Make sure we can overwrite a target list'''
    collector = server.get_collector_by_name('RodSerling')
    collector.set_target_cidrs(ipaddress.ip_network('10.201.0.7'))
    targets = collector.get_target_cidrs()
    assert ipaddress.ip_network('10.0.0.1') not in targets, "CIDR should not be in targets"

def test_invalid_cidr_type(server):
    '''Make sure we throw exceptions as expected'''
    collector = server.get_collector_by_name('RodSerling')
    try:
        collector._get_cidrs('foo')
    except spectreapi.InvalidArgument:
        assert True, "_get_cidrs('foo') raised an InvalidArgument"
        return
    assert False, "_get_cidrs('foo') should have raised an InvalidArgument"

def test_list_cidr(server):
    collector = server.get_collector_by_name('RodSerling')
    list = ['192.168.1.1/32', ipaddress.ip_network('192.168.1.2')]
    results = collector.set_avoid_cidrs(list)
    assert results.ok

def test_delete_cidr(server):
    collector = server.get_collector_by_name('RodSerling')
    add_list = ['192.168.1.3/32', ipaddress.ip_network('192.168.1.4'), '192.168.1.5/32']
    results = collector.set_avoid_cidrs(add_list)
    assert results.ok
    delete_list = ['192.168.1.3/32', '192.168.1.5/32']
    results = collector.delete_avoid_cidrs(delete_list)
    assert results.ok
    avoid_list = collector.get_avoid_cidrs()
    assert ipaddress.ip_network('192.168.1.3') not in avoid_list, "CIDR should not be in RodSerling avoids"
    assert ipaddress.ip_network('192.168.1.5') not in avoid_list, "CIDR should not be in RodSerling avoids"
    assert ipaddress.ip_network('192.168.1.4') in avoid_list, "CIDR should be in RodSerling avoids"

def test_delete_zone_cidr(server):
    zone = server.get_zone_by_name('Twilight')
    add_list = ['192.168.1.3/32', ipaddress.ip_network('192.168.1.4'), '192.168.1.5/32']
    results = zone.set_avoid_cidrs(add_list)
    assert results.ok
    delete_list = ['192.168.1.3/32', '192.168.1.5/32']
    results = zone.delete_avoid_cidrs(delete_list)
    assert results.ok
    avoid_list = zone.get_avoid_cidrs()
    assert ipaddress.ip_network('192.168.1.3') not in avoid_list, "CIDR should not be in RodSerling avoids"
    assert ipaddress.ip_network('192.168.1.5') not in avoid_list, "CIDR should not be in RodSerling avoids"
    assert ipaddress.ip_network('192.168.1.4') in avoid_list, "CIDR should be in RodSerling avoids"
