#!/usr/local/bin/python3

import requests
import json


class Server():
    session = requests.Session()
    server = ""
    url = ""
    cookies = {}

    def __init__(self, server, api_key):
        self.session.headers = {'Authorization': "Bearer " + api_key,
                                'Accept': 'json;pretty'}
        self.session.verify = False
        self.url = "https://" + server + "/api/rest/"
        self.session.timeout = 1

    def get(self, suffix, inparams):
        return self.session.get(self.url+suffix, params=inparams)


s = Server("i3", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMnsdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds")
