'''Module to test getting collector by name'''
def test_get_collector_by_name(server):
    '''Just what it says on the tin'''
    collector = server.get_collector_by_name('RodSerling')
    assert collector.id_num > 0, "There should be a collector by this name"
