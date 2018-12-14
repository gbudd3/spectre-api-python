'''Tests around collector.add_devices'''
import ipaddress

def device_host(ip, i):
    return { "@class" : "device",
             "ip" : str(ip),
             "phaseComplete" : False,
             "created" : 1535388219912 }

def device_snmpDiscovery(ip, i):
    return {
  "@class" : "device",
  "ip" : str(ip),
  "attributes" : [ {
    "name" : "sysLocation",
    "value" : "Unknown"
  }, {
    "name" : "sysDescr",
    "value" : "Lumeta Spectre Command Center version 3.3.0.12177 for lumeta_dev"
  }, {
    "name" : "sysServices",
    "value" : "end-to-end,application"
  }, {
    "name" : "SerialNumber",
    "value" : "serial" + str(ip)
  }, {
    "name" : "sysName",
    "value" : str(ip)
  }, {
    "name" : "sysObjectID",
    "value" : "1.3.6.1.4.1.48995.2.4.1"
  }, {
    "name" : "sysContact",
    "value" : "root@localhost"
  } ],
  "profileData" : [ {
    "type" : "sysObjectID",
    "data" : "1.3.6.1.4.1.48995.2.4.1",
    "port" : 0
  }, {
    "type" : "sysDescr",
    "data" : "Lumeta Spectre Command Center version 3.3.0.12177 for lumeta_dev",
    "port" : 0
  } ],
  "phaseComplete" : False,
  "created" : 1538390547675,
  "snmpAliases" : [ "alias" + str(i%5), "public" ],
}
def device_snmpDetail(ip,i):
    return {
  "@class" : "device",
  "ip" : str(ip),
  "interfaces" : [ {
    "index" : 1,
    "description" : "lo",
    "name" : "lo",
    "alias" : "",
    "adminStatus" : "up",
    "opStatus" : "up",
    "addresses" : [ "::", "127.0.0.1/8" ],
    "routes" : [ {
      "route" : "fe80::250:56ff:fe8e:b667",
      "nextHop" : "::",
      "type" : "local",
      "protocol" : "local",
      "ifIndex" : 1,
      "asNum" : 0
    }, {
      "route" : "2600:802:460:653:250:56ff:fe8e:b667",
      "nextHop" : "::",
      "type" : "local",
      "protocol" : "local",
      "ifIndex" : 1,
      "asNum" : 0
    }, {
      "route" : "::",
      "nextHop" : "::",
      "type" : "local",
      "protocol" : "local",
      "ifIndex" : 1,
      "asNum" : 0
    } ]
  }, {
    "index" : 3,
    "description" : "eth1",
    "name" : "eth1",
    "alias" : "",
    "adminStatus" : "up",
    "opStatus" : "up",
    "physicalAddress" : "00:50:56:8e:b6:67",
    "addresses" : [ "fe80::250:56ff:fe8e:b667/64", "2600:802:460:653:250:56ff:fe8e:b667/64", "172.16.53.129/25" ],
    "routes" : [ {
      "route" : "172.16.53.128/25",
      "type" : "local",
      "protocol" : "local",
      "ifIndex" : 3,
      "asNum" : 0
    }, {
      "route" : "::/0",
      "type" : "remote",
      "protocol" : "local",
      "ifIndex" : 3,
      "asNum" : 0
    }, {
      "route" : "fe80::/64",
      "nextHop" : "::",
      "type" : "local",
      "protocol" : "local",
      "ifIndex" : 3,
      "asNum" : 0
    }, {
      "route" : "2600:802:460:653::/64",
      "nextHop" : "::",
      "type" : "local",
      "protocol" : "local",
      "ifIndex" : 3,
      "asNum" : 0
    }, {
      "route" : "169.254.0.0/16",
      "type" : "local",
      "protocol" : "local",
      "ifIndex" : 3,
      "asNum" : 0
      }, {
      "route" : "172.16.53.128",
      "type" : "local",
      "protocol" : "local",
      "ifIndex" : 3,
      "asNum" : 0
    }, {
      "route" : "ff00::/8",
      "nextHop" : "::",
      "type" : "local",
      "protocol" : "local",
      "ifIndex" : 3,
      "asNum" : 0
    } ],
    "hosts" : [ {
      "mac" : "54:75:d0:19:4a:3f",
      "ip" : "fe80::5675:d0ff:fe19:4a3f"
    }, {
      "mac" : "00:50:56:8e:d4:00",
      "ip" : "172.16.53.130"
    } ]
  }, {
    "index" : 2,
    "description" : "eth0",
    "name" : "eth0",
    "alias" : "",
    "adminStatus" : "up",
    "opStatus" : "up",
    "physicalAddress" : "00:50:56:8e:61:23",
    "addresses" : [ str(ip)+"/24" ],
    "routes" : [ {
      "route" : str(ip) + "/24",
      "type" : "local",
      "protocol" : "local",
      "ifIndex" : 2,
      "asNum" : 0
    }, {
      "route" : "0.0.0.0/0",
      "type" : "remote",
      "protocol" : "local",
      "ifIndex" : 2,
      "asNum" : 0
          }, {
      "route" : "172.16.53.0",
      "type" : "local",
      "protocol" : "local",
      "ifIndex" : 2,
      "asNum" : 0
    }, {
      "route" : "169.254.0.0",
      "type" : "local",
      "protocol" : "local",
      "ifIndex" : 2,
      "asNum" : 0
    }, {
      "route" : "169.254.0.0/16",
      "type" : "local",
      "protocol" : "local",
      "ifIndex" : 2,
      "asNum" : 0
    }, {
      "route" : "0.0.0.0/0",
      "nextHop" : "172.16.53.1",
      "type" : "remote",
      "protocol" : "local",
      "ifIndex" : 2,
      "asNum" : 0
    } ],
    "hosts" : [ {
      "mac" : "54:75:d0:19:4a:3f",
      "ip" : "172.16.53.1"
    } ]
  } ],
    "attributes" : [ {
    "name" : "RFC4292",
    "value" : "true"
  }, {
    "name" : "sysContact",
    "value" : "Root <root@localhost> (configure /etc/snmp/snmp.local.conf)"
  }, {
    "name" : "sysDescr",
    "value" : "Linux i10.corp.lumeta.com 2.6.32-573.el6.x86_64 #1 SMP Thu Jul 23 15:44:03 UTC 2015 x86_64"
  }, {
    "name" : "sysObjectID",
    "value" : "1.3.6.1.4.1.8072.3.2.10"
  }, {
    "name" : "sysName",
    "value" : "i10.corp.lumeta.com"
  }, {
    "name" : "sysLocation",
    "value" : "Unknown (edit /etc/snmp/snmpd.conf)"
  }, {
    "name" : "RFC2096",
    "value" : "true"
  } ],
  "profileData" : [ {
    "type" : "sysDescr",
    "data" : "Linux i10.corp.lumeta.com 2.6.32-573.el6.x86_64 #1 SMP Thu Jul 23 15:44:03 UTC 2015 x86_64",
    "port" : 0
  }, {
    "type" : "sysObjectID",
    "data" : "1.3.6.1.4.1.8072.3.2.10",
    "port" : 0
  } ],
  "phaseComplete" : False,
  "created" : 1538442765877,
  "snmpAliases" : [ "aliasforpublic" ]
  }

def device_dns(ip,i):
        return {
            "@class" : "device",
            "ip" : str(ip),
            "attributes" : [ {
                "name" : "dnsname",
                "value" : "gnarled.mellon." + str(ip) + ".com"
            } ],
            "phaseComplete" : False,
            "created" : 1538421241211,
            }

def device_tcp(ip,i):
    return {
        "@class" : "device",
        "ip" : str(ip),
        "profileData" : [ {
            "type" : "tcp",
            "data" : "tcpsynack:4:64:0:1460:mss*10,7:mss,nop,nop,ts,nop,ws:df:0"
        } ],
        "phaseComplete" : True,
        "created" : 1538421240160,
        "closedTcpPorts" : [ 113, 1041, 1047, 88, 1002, 1036, 79 ],
        "openTcpPorts" : [ 80, 443 ]
        }

def test_add_10k_devices(server):
    '''Test adding 10K single devices'''
    zone = setup_zone(server)
    collector = setup_collector('Demilitarized', server, server._host, zone)
    hostDiscovery = DeviceWriter(collector, device_host, 'hostDiscovery', 'icmp')
    snmpDiscovery = DeviceWriter(collector, device_snmpDiscovery, 'snmpDiscovery', 'snmpv2')
    snmpDetail = DeviceWriter(collector, device_snmpDetail, 'snmpDetails', 'snmpv2')
    dnsDiscovery = DeviceWriter(collector, device_dns, 'dns', 'unspecified')
    tcpDiscovery = DeviceWriter(collector, device_tcp, 'tcpPorts', 'tcp')
    
    i = 0
    devices = { 'devices' : [] }
    network = ipaddress.ip_network('10.0.0.0/8')
    for ip in network:
        hostDiscovery.add(ip)
        snmpDiscovery.add(ip)
        snmpDetail.add(ip)
        dnsDiscovery.add(ip)
        tcpDiscovery.add(ip)
        i += 1
        if i == 10000:
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


