'''Test chunking cidrs '''
import ipaddress
import spectreapi

def test_chunked_collector_set_cidr(server):
    '''Make sure we chunk set*cidr calls'''

    collector = server.get_collector_by_name('RodSerling')
    avoid = list(ipaddress.ip_network('192.168.1.0/26').hosts())[0:10]
    collector.set_avoid_cidrs(*avoid,chunk_size=3)
    avoided = collector.get_avoid_cidrs()
    assert str(avoided[9]) == '192.168.1.10/32', "The last avoided cidr should have been 192.168.1.10"

def test_chunked_zone_set_cidr(server):
    '''Make sure we chunk set*cidr calls'''

    zone = server.get_zone_by_name('Twilight')
    avoid = list(ipaddress.ip_network('192.168.1.0/26').hosts())[0:10]
    zone.set_avoid_cidrs(*avoid,chunk_size=3)
    avoided = zone.get_avoid_cidrs()
    assert str(avoided[9]) == '192.168.1.10/32', "The last avoided cidr should have been 192.168.1.10"
