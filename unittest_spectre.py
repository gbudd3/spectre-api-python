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
            
class TestPageSizes(unittest.TestCase):
    def test_pagesizes(self):
        s = spectre.APIKeyServer(
            "i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlI" +
            "joxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMn" +
            "sdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds")
        r = s.getpage("zonedata/devices", params={"filter.zone.id": "4"})
        correct_count = r.json()['total']

        for size in (1, 2, 5, 7, 500):
            s = spectre.APIKeyServer(
                "i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlI" +
                "joxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMn" +
                "sdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds", page_size=size)

            r = s.get("zonedata/devices", params={"filter.zone.id": "4"})

            count = 0
            for d in r:
                count += 1
            self.assertEqual(correct_count, count, 'Count should be the same at page size %d' % size)
