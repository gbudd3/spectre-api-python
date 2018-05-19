'''Setup for all the tests'''
import spectreapi
import pytest

@pytest.fixture()
def server():
    '''Just sets up a server'''
    return spectreapi.UsernameServer('6hour', 'admin', 'admin')
