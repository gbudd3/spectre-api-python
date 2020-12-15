#!/usr/local/bin/python3

import argparse
import spectreapi
import ipaddress
import time
import sys

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--host')
    parser.add_argument('-d','--debug',action='store_true')
    args = parser.parse_args()
    if args.host is None:
        print("Hostname (--host) is required")
        sys.exit(1)

    host = args.host
    debug = args.debug


    server = spectreapi.UsernameServer(host, 'username', 'password')

    # Creating a zone is pretty easy, via get_or_create_zone
    zone = server.get_or_create_zone('Example 1')

    # The setup_collector function below is a little more complicated
    # but at its heart is a server.post to zone/collector with a JSON payload with the collector config
    collector = setup_collector('Example 1', server, host, zone)

    # You can get a config by running 
    # c = server.query("zone/collector").filter('collector.name','Example 1').detail("Config").run().result
    # or a more human readable one by running:
    # print(json.dumps(server.query("zone/collector").filter('collector.name','Zone1').detail("Config").run().result, indent=4))


    collector.set_target_cidrs('10.101.1.0/24', '10.101.2.0/24', '172.18.1.0/24')


def setup_collector(collector_name, server,host,zone):

    collector = server.get_collector_by_name(collector_name)
    if collector:
        return collector

    data = '''
        [ 
        {
            "@class": "collector",
            "name": "Example 1",
            "zone": {
                  "id": %d,
                  "name": "Example 1"
             },
            "discoveryInterface" : {
                "name" : "%s:eth2",
                "type" : "ETHERNET",
                "active" : true,
                "config" : "manual/10000/full",
                "ospf" : { }
            },
            "enabled": true,
            "rescanInterval": 1,
            "hostDiscovery": {
                "enabled": true,
                "icmp": true,
                 "dns": true,
                 "snmp": true,
                 "udp": true,
                 "tcpPorts": [22]
            },
            "snmpDiscovery": {
                    "collectInterfaces": true,
                    "collectLayer2Data": true,
                    "collectRoutes": true,
                    "skipBgpRoutes": false,
                    "useCommonCredentials": true,
                    "extraCredentials": [
                        {
                            "community": "CISCO",
                            "alias": "CISCO"
                        },
                        {
                            "community": "public",
                            "alias": "public"
                        },
                        {
                            "community": "read",
                            "alias": "read"
                        },
                        {
                            "community": "private",
                            "alias": "private"
                        },
                        {
                            "community": "community",
                            "alias": "community"
                        },
                        {
                            "community": "password",
                            "alias": "password"
                        },
                        {
                            "community": "guest",
                            "alias": "guest"
                        },
                        {
                            "community": "switch",
                            "alias": "switch"
                        },
                        {
                            "community": "tivoli",
                            "alias": "tivoli"
                        },
                        {
                            "community": "SUN",
                            "alias": "SUN"
                        },
                        {
                            "community": "seri",
                            "alias": "seri"
                        },
                        {
                            "community": "foobar",
                            "alias": "foobar"
                        },
                        {
                            "community": "world",
                            "alias": "world"
                        },
                        {
                            "community": "scotty",
                            "alias": "scotty"
                        },
                        {
                            "community": "admin",
                            "alias": "admin"
                        },
                        {
                            "community": "ILMI",
                            "alias": "ILMI"
                        },
                        {
                            "community": "root",
                            "alias": "root"
                        },
                        {
                            "community": "manager",
                            "alias": "manager"
                        },
                        {
                            "community": "access",
                            "alias": "access"
                        },
                        {
                            "community": "SNMP",
                            "alias": "SNMP"
                        },
                        {
                            "community": "openview",
                            "alias": "openview"
                        },
                        {
                            "community": "proxy",
                            "alias": "proxy"
                        },
                        {
                            "community": "monitor",
                            "alias": "monitor"
                        },
                        {
                            "community": "2read",
                            "alias": "2read"
                        },
                        {
                            "community": "snmp",
                            "alias": "snmp"
                        },
                        {
                            "community": "ctron",
                            "alias": "ctron"
                        },
                        {
                            "community": "default",
                            "alias": "default"
                        },
                        {
                            "community": "network",
                            "alias": "network"
                        },
                        {
                            "community": "mngt",
                            "alias": "mngt"
                        },
                        {
                            "community": "write",
                            "alias": "write"
                        },
                        {
                            "community": "router",
                            "alias": "router"
                        },
                        {
                            "community": "4changes",
                            "alias": "4changes"
                        },
                        {
                            "community": "snmpd",
                            "alias": "snmpd"
                        },
                        {
                            "community": "system",
                            "alias": "system"
                        },
                        {
                            "community": "secret",
                            "alias": "secret"
                        }
                    ],
                    "enabled": true
                },
            "portDiscovery": {
                "enabled": true,
                "useVulnerablePorts": true,
                "useInfectionPorts": true,
                "tcpPorts": [ 25 ]
            },
            "profileDiscovery": {
                "collectHTTP": true,
                "collectCIFS": true,
                "httpPorts": [ 80 ],
                "httpsPorts": [ 443 ]
            },
            "dnsDiscovery": {
                "enabled": true,
                "useSystemDNSServer": true,
                "internalDNSServers": [],
                "externalEnabled": false,
                "externalDNSServers": [],
                "issueForwardQueriesV4": true,
                "issueForwardQueriesV6": true
            },
            "cloudDiscovery": {},
            "wmiDiscovery": {},
            "cidrUpdated": 0
        }
 ] ''' % ( zone.id_num, host )
    r = server.post("zone/collector", data=data);
    collector = server.get_collector_by_name(collector_name)
    return collector

main()


