#!/usr/local/bin/python3

import requests
import json


class Server():
    """
    A Server is used to make API Calls to a Lumeta Spectre server 
    """

    def __init__(self, server):
        self.session = requests.Session()
        self.session.verify = False
        self.url = "https://" + server + "/api/rest/"
        self.session.timeout = 1

    def get(self, api, params=None):
        """
        """
        r = self.session.get(self.url+api, params=params,timeout=5)
        return r

class APIKeyServer(Server):
    """
    An APIKeyServer is a Server that uses authentication via API key.
    You get an API key from the CLI via the "user key new <username>" command
    """

    def __init__(self,server,api_key):
            """
            APIKeyServer(server,api_key) where
            server is the Spectre server you're connecting to and
            api_key is the API key you've generated
            """
            super().__init__(server)
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

