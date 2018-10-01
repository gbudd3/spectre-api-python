'''Tests around collector.add_devices'''
import ipaddress

def device_host(ip, i):
    return { "@class" : "device",
             "ip" : str(ip),
             "phaseComplete" : False,
             "created" : 1535388219912 }


def test_add_10k_devices(server):
    '''Test adding 10K single devices'''
    zone = setup_zone(server)
    collector = setup_collector('Demilitarized', server, server._host, zone)
    hostDiscovery = DeviceWriter(collector, device_host, 'hostDiscovery', 'icmp')
    
    i = 0
    devices = { 'devices' : [] }
    network = ipaddress.ip_network('10.0.0.0/8')
    for ip in network:
        hostDiscovery.add(ip)
        i += 1
        if i == 1000:
            break


    results = zone.query().filter('address.ip','1.0.0.255').run()
    assert results.values(), "There should be a 10.0.0.255, we just added it"

def device_host(ip, i):
    return { "@class" : "device",
             "ip" : str(ip),
             "phaseComplete" : False,
             "created" : 1535388219912 }

class DeviceWriter:
    def __init__(self, collector, device_function, scan_type, protocol, batch_size=100):
        self.collector = collector
        self.device_function = device_function
        self.scan_type = scan_type
        self.protocol = protocol
        self.batch_size = batch_size
        self.i = 0
        self.devices = { 'devices' : [] }

    def add(self,ip):
        self.devices['devices'].append( self.device_function(ip, self.i))
        self.i += 1
        if self.i % self.batch_size == 0:
            self.collector.add_devices(self.devices, scanType=self.scan_type, protocol=self.protocol)
            self.devices = { 'devices' : [] }    
            
 
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


