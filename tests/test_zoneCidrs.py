import ipaddress

def test_setCidrs(server):
    zones = server.getZones()
    zone = zones[1]

    assert zone.setKnownCidrs(ipaddress.ip_network('1.1.1.1')).ok == True
    assert zone.setKnownCidrs('1.1.1.2',append=True).ok == True
    assert zone.setEligibleCidrs('2.2.2.2').ok == True
    assert zone.setTrustedCidrs('2.2.2.3',append=True).ok == True
    assert zone.setInternalCidrs('3.3.3.3').ok == True

def test_getCidrs(server):
    zones = server.getZones()
    zone = zones[1]

    c = zone.getKnownCidrs()
    assert ipaddress.ip_network('1.1.1.1/32') in c
    assert ipaddress.ip_network('1.1.1.2/32') in c

    c1 = zone.getEligibleCidrs()
    c2 = zone.getTrustedCidrs()
    assert c1 == c2
    assert ipaddress.ip_network('2.2.2.2/32') in c1
    assert ipaddress.ip_network('2.2.2.3/32') in c1

    c = zone.getInternalCidrs()
    assert ipaddress.ip_network('3.3.3.3/32') in c
