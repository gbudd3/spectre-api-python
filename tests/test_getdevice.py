import pytest
import spectreapi

def test_nodevice(server):

    zone = server.get_zone_by_name('Twilight')
    results = zone.get_device_details_by_ip('1.1.1.1')
    assert len(results.values()) == 0, "There shouldn't be any results if we don't find the IP"

def test_hasdevice(server):
    zone = server.get_zone_by_name('Twilight')
    results = zone.get_device_details_by_ip('172.16.22.41')
    assert len(results.values()) == 1, "There should be a results for this IP"
