'''Tests around get_device_details_by_ip'''

def test_query(server):
    '''Test what an query looks like'''
    devices = server.query().filter('zone.id',2).run()
    for device in devices:
        assert device['id'] > 0, "All devices should have an id"

