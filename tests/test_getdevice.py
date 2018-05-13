import pytest
import spectreapi

def test_nodevice(server):

    zone = server.getZoneByName('Twilight')
    results = zone.getDeviceDetailsByIP('1.1.1.1')
    assert len(results.values()) == 0, "There shouldn't be any results if we don't find the IP"

def test_hasdevice(server):
    zone = server.getZoneByName('Twilight')
    result = zone.getDeviceDetailsByIP('172.16.22.41')
    assert result.result()['active'], "This should be an active device"
