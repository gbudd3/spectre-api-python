'''Tests around API Key Server access'''
import spectreapi

def test_createserver():
    '''Create server'''
    server = spectreapi.APIKeyServer(
        "i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlI" +
        "joxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMn" +
        "sdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds")
    results = server.getpage("system/information")
    server_results = results.json()['results'][0]

    assert results.json()['status'] == 'SUCCESS'
    assert server_results['name'] == 'i3'

def test_pagesizes():
    '''Test server access with different page sizes'''
    server = spectreapi.APIKeyServer(
        "i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlI" +
        "joxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMn" +
        "sdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds")
    results = server.getpage("zonedata/devices", params={"filter.zone.id": "4"})
    correct_count = results.json()['total']
    server.close()

    for size in (1, 2, 5, 7, 500):
        server = spectreapi.APIKeyServer(
            "i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlI" +
            "joxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMn" +
            "sdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds", page_size=size)

        results = server.get("zonedata/devices", params={"filter.zone.id": "4"})

        count = 0
        for _ in results:
            count += 1
        server.close()
        assert correct_count == count

def test_rewind():
    '''Test the ability to rewind the results and re-iterate over them'''
    server = spectreapi.APIKeyServer(
        "i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlI" +
        "joxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMn" +
        "sdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds")
    results = server.get("zonedata/devices", params={"filter.zone.id": "4"})
    count1 = 0
    for _ in results:
        count1 += 1

    count2 = 0
    for _ in results:
        count2 += 1

    server.close()
    assert count1 == count2
