#!/usr/local/bin/python3
"""
The spectre module is used to make access to Lumeta's Spectre API
a little easier.
"""
import math
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Server():
    """
    A Server is used to make API Calls to a Lumeta Spectre(r) server
    """

    def __init__(self, server, page_size=500):
        self.session = requests.Session()
        self.session.verify = False
        self.page_size = page_size
        self.url = "https://" + server + "/api/rest/"
        self.session.timeout = 1

    def _get(self, api, params=None, page=1):
        """
        This private method is in place to handle the actual
        fetching of GET API calls
        """
        if params is None:
            params = {"query.pagesize": self.page_size}

        params["query.pagesize"] = self.page_size
        params["query.page"] = page
        r = self.session.get(self.url+api, params=params, timeout=5)
        return r

    def get(self, api, params=None):
        """
        Use this method to GET results from an API call
        """
        return Response(self, api, params)


class Response():
    """
    This class is used to present the results of a "GET" API call
    """

    def __init__(self, server, api, params):
        self.server = server
        self.api = api
        self.params = params
        self.page = 0
        self.page_line = 0
        self.r = self.server._get(api, params, page=self.page)

        if "total" in self.r.json():
            self.total = self.r.json()['total']
        else:
            self.total = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.page * self.server.page_size + self.page_line == self.total:
            raise StopIteration

        if self.page_line < self.server.page_size:
            self.page_line += 1
            try:
                return self.r.json()['results'][self.page_line - 1]
            except IndexError:
                raise StopIteration # This could happen if the underlying query shrinks under us

        else:
            self.page_line = 1
            self.page += 1
            self.r = self.server._get(self.api, self.params, page=self.page)
            try:
                return self.r.json()['results'][0]
            except IndexError:
                raise StopIteration # This could happen if the underlying query shrinks under us

    def pages(self):
        return math.ceil(self.total / self.server.page_size)



class APIKeyServer(Server):
    """
    An APIKeyServer is a Server that uses authentication via API key.
    You get an API key from the CLI via the "user key new <username>" command
    """

    def __init__(self, server, api_key, page_size=500):
        """
        APIKeyServer(server,api_key) where
        server is the Spectre server you're connecting to and
        api_key is the API key you've generated

        >>> import spectre
        >>> s = APIKeyServer("i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"+ \
                ".eyJkYXRlIjoxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMns"+ \
                "dPAG6l3oinHOjPFAfsfUkgOs0YKyhwds")
        >>> r = s._get("system/information")
        >>> r.json()['status']
        'SUCCESS'
        >>> r.json()['results'][0]['name']
        'i3'
        """
        super().__init__(server, page_size=page_size)
        self.session.headers = {'Authorization': "Bearer " + api_key,
                                'Accept': 'json;pretty'}


if __name__ == '__main__':

    s = APIKeyServer(
        "i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlI" +
        "joxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMn" +
        "sdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds", page_size=5)
    r1 = s._get("system/information")
    print(r1.headers)
    print(r1.text)

    r2 = s._get("zonedata/devices", params={"filter.zone.id": "4"})
    print(r2.headers)
    print(r2.text)

    r3 = s.get("zonedata/devices", params={"filter.zone.id": "4"})
    count = 0
    for d in r3:
        count += 1
        print("%d %s" % (count, d['mac']))
    print("Total count of devices: %d" % count)


