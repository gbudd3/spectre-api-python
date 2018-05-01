import unittest
import spectre

class TestAPIKeyServer(unittest.TestCase):
    def test_createserver(self):
        s = spectre.APIKeyServer(
            "i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlI" +
            "joxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMn" +
            "sdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds")
        r = s.getpage("system/information")
        v = r.json()['results'][0]

        self.assertEqual(r.json()['status'], 'SUCCESS', 'Status should be successful')
        self.assertEqual(v['name'],'i3','Name should be correct')
        s.close()
            
class TestPageSizes(unittest.TestCase):
    def test_pagesizes(self):
        s = spectre.APIKeyServer(
            "i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlI" +
            "joxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMn" +
            "sdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds")
        r = s.getpage("zonedata/devices", params={"filter.zone.id": "4"})
        correct_count = r.json()['total']
        s.close()

        for size in (1, 2, 5, 7, 500):
            s = spectre.APIKeyServer(
                "i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlI" +
                "joxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMn" +
                "sdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds", page_size=size)

            r = s.get("zonedata/devices", params={"filter.zone.id": "4"})

            count = 0
            for d in r:
                count += 1
            s.close()
            self.assertEqual(correct_count, count, 'Count should be the same at page size %d' % size)

class TestRewind(unittest.TestCase):
    def test_rewind(self):
        s = spectre.APIKeyServer(
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
        self.assertEqual(count1, count2, "Count should be equal every time through the iteration")

class TestUsernameServer(unittest.TestCase):
    def test_usernameserver(self):
        r = spectre.UsernameServer("i3", "admin", "admin").get("zonedata/devices", params={"filter.zone.id": "4"})
        r.server.session.close()
        self.assertEqual(r.result()['@class'], "device", "@class should be device")

    def test_usernameserverpaging(self):
        r = spectre.UsernameServer("i3", "admin", "admin").get("zonedata/devices", params={"filter.zone.id": "4"})
        count1 = 0
        for d in r:
            count1 += 1

        r.server.session.close()
        self.assertEqual(count1, r.total, "Count of records should equal r.total")