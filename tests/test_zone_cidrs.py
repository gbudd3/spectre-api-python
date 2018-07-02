'''Tests around zone CIDRs'''
import ipaddress
import spectreapi

def test_set_cidrs(server):
    '''Set CIDRs and make sure they return ok'''
    zone = server.get_zone_by_name('Twilight')

    assert zone.set_known_cidrs(ipaddress.ip_network('1.1.1.1')).ok
    assert zone.set_known_cidrs('1.1.1.2', append=True).ok
    assert zone.set_eligible_cidrs('2.2.2.2').ok
    assert zone.set_trusted_cidrs('2.2.2.3', append=True).ok
    assert zone.set_internal_cidrs('3.3.3.3').ok

def test_get_cidrs(server):
    '''Get CIDRs and make sure they match what we added'''
    zone = server.get_zone_by_name('Twilight')

    cidrs = zone.get_known_cidrs()
    assert ipaddress.ip_network('1.1.1.1/32') in cidrs
    assert ipaddress.ip_network('1.1.1.2/32') in cidrs

    known_cidrs = zone.get_eligible_cidrs()
    trusted_cidrs = zone.get_trusted_cidrs()
    assert known_cidrs == trusted_cidrs
    assert ipaddress.ip_network('2.2.2.2/32') in known_cidrs
    assert ipaddress.ip_network('2.2.2.3/32') in known_cidrs

    internal_cidrs = zone.get_internal_cidrs()
    assert ipaddress.ip_network('3.3.3.3/32') in internal_cidrs

def test_get_bad_cidr_type(server):
    '''Test what happens when we make a request for an invalid CIDR type'''
    zone = server.get_zone_by_name('Twilight')
    try:
        zone._get_cidrs('foo')
    except spectreapi.InvalidArgument:
        assert True
        return

    assert False

def test_missing_server(server):
    '''Test what happens when we make a request from a zone without a server'''
    zone = server.get_zone_by_name('Twilight')
    try:
        zone.server = None
        zone.get_known_cidrs()
    except spectreapi.NoServerException:
        assert True
        return

    assert False

def test_zone_list_cidr(server):
    zone = server.get_zone_by_name('Twilight')
    list = ['192.168.1.100/32', ipaddress.ip_network('192.168.1.101')]
    results = zone.set_avoid_cidrs(list)
    assert results.ok
    avoided = zone.get_avoid_cidrs()
    assert ipaddress.ip_network('192.168.1.100')  in avoided, "Check that string was added"
    assert ipaddress.ip_network('192.168.1.101')  in avoided, "Check that list of string was added"
