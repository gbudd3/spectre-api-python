#!/usr/local/bin/python3

import requests
import json


class Server():

    def __init__(self, server, *, api_key=None, username=None, password=None, cert=None):
        self.session = requests.Session()
        if api_key:
            self.session.headers = {'Authorization': "Bearer " + api_key,
                                    'Accept': 'json;pretty'}

        self.session.verify = False
        self.url = "https://" + server + "/api/rest/"
        self.session.timeout = 1

    def get(self, api, inparams=None):
        r = self.session.get(self.url+api, params=inparams,timeout=5)
        r.raise_for_status()
        return r


s = Server("i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMnsdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds")
