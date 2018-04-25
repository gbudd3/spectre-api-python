#!/usr/local/bin/python3

import requests
import json


class Server():

    def __init__(self, server):
        self.session = requests.Session()
        self.session.verify = False
        self.url = "https://" + server + "/api/rest/"
        self.session.timeout = 1

    def get(self, api, params=None):
        r = self.session.get(self.url+api, params=params,timeout=5)
        return r

class APIKeyServer(Server):

    def __init__(self,server,api_key):
            super(APIKeyServer,self).__init__(server)
            self.session.headers = {'Authorization': "Bearer " + api_key,
                                    'Accept': 'json;pretty'}



if __name__ == '__main__': 

    s = APIKeyServer("i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMnsdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds")
    r=s.get("system/information")
    print(r.headers)
    print(r.text)

    r=s.get("zonedata/devices",params={"filter.zone.id":"4"})
    print(r.headers)
    print(r.text)

