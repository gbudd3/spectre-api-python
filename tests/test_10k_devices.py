'''Tests around collector.add_devices'''
import ipaddress

def test_add_10k_devices(server):
    '''Test adding 10K single devices'''
    zone = setup_zone(server)
    collector = setup_collector('Demilitarized', server, server._host, zone)
    
    i = 0
    devices = { 'devices' : [] }
    network = ipaddress.ip_network('10.0.0.0/8')
    for ip in network:
        device = { "@class" : "device",
                "ip" : str(ip),
                "phaseComplete" : False,
                "created" : 1535388219912 }
        devices['devices'].append(device)
        i += 1
        if i % 100 == 0:
            collector.add_devices(devices)
            devices = { 'devices' : [] }

        if i == 10000:
            break


    results = zone.query().filter('address.ip','1.0.0.255').run()
    assert results.values(), "There should be a 10.0.0.255, we just added it"

 
def setup_zone(server):
    zone = server.get_zone_by_name('Demilitarized')
    if zone:
        return zone

    data = '''
        [{
            "@class":"zone",
            "name":"Demilitarized",
            "description": "Zone to Test Creating Devices",
            "organization":{"id":1, "name":"Test Organization"}
        }]
        '''
    r = server.post("zone", data=data);
    zone = server.get_zone_by_name('Demilitarized')
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
            "name" : "Demilitarized"
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


