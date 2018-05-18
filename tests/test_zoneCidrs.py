import ipaddress

def test_setCidrs(server):
    zone = server.get_zone_by_name('Twilight')

    assert zone.set_known_cidrs(ipaddress.ip_network('1.1.1.1')).ok == True
    assert zone.set_known_cidrs('1.1.1.2',append=True).ok == True
    assert zone.set_eligible_cidrs('2.2.2.2').ok == True
    assert zone.set_trusted_cidrs('2.2.2.3',append=True).ok == True
    assert zone.set_internal_cidrs('3.3.3.3').ok == True

def test_getCidrs(server):
    zone = server.get_zone_by_name('Twilight')

    c = zone.get_known_cidrs()
    assert ipaddress.ip_network('1.1.1.1/32') in c
    assert ipaddress.ip_network('1.1.1.2/32') in c

    c1 = zone.get_eligible_cidrs()
    c2 = zone.get_trusted_cidrs()
    assert c1 == c2
    assert ipaddress.ip_network('2.2.2.2/32') in c1
    assert ipaddress.ip_network('2.2.2.3/32') in c1

    c = zone.get_internal_cidrs()
    assert ipaddress.ip_network('3.3.3.3/32') in c
