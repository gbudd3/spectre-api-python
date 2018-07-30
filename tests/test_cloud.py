'''Tests around get_device_details_by_ip'''

def test_awsdevice(server):
    '''Test what an AWS device looks like'''
    zone = server.get_zone_by_name('Twilight')
    results = zone.query().filter('address.ip','1.1.1.1')
    assert not results.values(), "There shouldn't be any results if we don't find the IP"

