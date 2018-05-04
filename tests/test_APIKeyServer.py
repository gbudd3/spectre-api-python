import spectreapi

def test_createserver():
    s = spectreapi.APIKeyServer(
        "i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlI" +
        "joxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMn" +
        "sdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds")
    r = s.getpage("system/information")
    v = r.json()['results'][0]

    assert r.json()['status'] == 'SUCCESS'
    assert v['name'] == 'i3'
            
def test_pagesizes():
    s = spectreapi.APIKeyServer(
        "i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlI" +
        "joxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMn" +
        "sdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds")
    r = s.getpage("zonedata/devices", params={"filter.zone.id": "4"})
    correct_count = r.json()['total']
    s.close()

    for size in (1, 2, 5, 7, 500):
        s = spectreapi.APIKeyServer(
            "i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlI" +
            "joxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMn" +
            "sdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds", page_size=size)

        r = s.get("zonedata/devices", params={"filter.zone.id": "4"})

        count = 0
        for d in r:
            count += 1
        s.close()
        assert correct_count == count

def test_rewind():
    s = spectreapi.APIKeyServer(
        "i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlI" +
        "joxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMn" +
        "sdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds")
    r = s.get("zonedata/devices", params={"filter.zone.id": "4"})
    count1 = 0
    for d in r:
        count1 += 1

    count2 = 0
    for d in r:
        count2 += 1

    s.close()
    assert count1 == count2


