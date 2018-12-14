'''Tests around collector.add_devices'''

def test_add_device(server):
    '''Test adding a single device'''
    zone = setup_zone(server)
    collector = setup_collector('DemilitarizedPip', server, server._host, zone)
    device = { "@class" : "device",
            "ip" : "1.1.1.1",
            "phaseComplete" : False,
            "created" : 1535388219912 }
    collector.add_devices(device)

    results = zone.query().filter('address.ip','1.1.1.1').run()
    assert results.values(), "There should be a 1.1.1.1, we just added it"

def test_add_devices(server):
    '''Test adding a multiple devices'''
    zone = setup_zone(server)
    collector = setup_collector('DemilitarizedPip', server, server._host, zone)
    devices = {'devices' : [ 
        { "@class" : "device",
            "ip" : "1.1.1.2",
            "phaseComplete" : False,
            "created" : 1535388219912 },
        { "@class" : "device",
            "ip" : "1.1.1.3",
            "phaseComplete" : False,
            "created" : 1535388219912 } 
        ] }
    collector.add_devices(devices)

    results = zone.query().filter('address.ip','1.1.1.2').run()
    assert results.values(), "There should be a 1.1.1.2, we just added it"
    results = zone.query().filter('address.ip','1.1.1.3').run()
    assert results.values(), "There should be a 1.1.1.3, we just added it"

 
 
def setup_zone(server):
    zone = server.get_zone_by_name('DemilitarizedPip')
    if zone:
        return zone

    data = '''
        [{
            "@class":"zone",
            "name":"DemilitarizedPip",
            "description": "Zone to Test Creating Devices",
            "organization":{"id":1, "name":"Test Organization"}
        }]
        '''
    r = server.post("zone", data=data);
    zone = server.get_zone_by_name('DemilitarizedPip')
    return zone

def setup_collector(collector_name, server,host,zone):
    collector = server.get_collector_by_name(collector_name)
    if collector:
        return collector

    data = '''
        [ {
            "@class" : "collector",
            "name" : "%s",
            "discoveryInterface" : {
            "name" : "%s:eth0",
            "type" : "ETHERNET",
            "active" : true,
            "config" : "manual/10000/full",
            "ospf" : { }
            },
            "zone" : {
            "id" : %d,
            "name" : "DemilitarizedPip"
            },
            "enabled" : true,
            "rescanInterval" : 150,
            "hostDiscovery" : {
                "enabled" : true,
                "icmp" : true,
                "dns" : false,
                "snmp" : false,
                "udp" : false
            }
            } ] ''' % (collector_name, host, zone.id_num)
    r = server.post("zone/collector", data=data);
    #print(r.text)
    collector = server.get_collector_by_name(collector_name)
    return collector


