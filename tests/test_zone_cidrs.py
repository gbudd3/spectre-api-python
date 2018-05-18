import ipaddress

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
