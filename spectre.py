#!/usr/local/bin/python3
"""
The spectre module is used to make access to Lumeta's Spectre API
a little easier.
"""
import math
import requests
import urllib3



class Server():
    """
    A Server is used to make API Calls to a Lumeta Spectre(r) server
    """

    def __init__(self, server, page_size=500, verify_cert=False):
        self.session = requests.Session()
        self.session.verify = False
        self.page_size = page_size
        self.url = "https://" + server + "/api/rest/"
        self.session.timeout = 1
        if verify_cert is False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def close(self):
        self.session.close()

    def getpage(self, api, params=None, page=0):
        """
        This private method is in place to handle the actual
        fetching of GET API calls
        """
        if params is None:
            params = {"query.pagesize": self.page_size}

        params["query.pagesize"] = self.page_size
        params["query.page"] = page
        results = self.session.get(self.url+api, params=params, timeout=5)
        return results

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
        self.results = self.server.getpage(api, params, page=self.page)

        if "total" in self.results.json():
            self.total = self.results.json()['total']
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
                return self.results.json()['results'][self.page_line - 1]
            except IndexError:
                raise StopIteration # This could happen if the underlying query shrinks under us

        else:
            self.page_line = 1
            self.page += 1
            self.results = self.server.getpage(self.api, self.params, page=self.page)
            try:
                return self.results.json()['results'][0]
            except IndexError:
                raise StopIteration # This could happen if the underlying query shrinks under us

    def pages(self):
        """Return the highest page number (starting from page 0)"""
        return math.ceil(self.total / self.server.page_size)

    def values(self):
        """Return the values from the API call"""
        return self.results.json()['results']



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
        >>> r = s.getpage("system/information")
        >>> r.json()['status']
        'SUCCESS'
        >>> r.json()['results'][0]['name']
        'i3'
        """
        super().__init__(server, page_size=page_size)
        self.session.headers = {'Authorization': "Bearer " + api_key,
                                'Accept': 'json;pretty'}


if __name__ == '__main__':

    S = APIKeyServer(
        "i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlI" +
        "joxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMn" +
        "sdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds", page_size=500)

    R1 = S.getpage("system/information")
    print(R1.headers)
    print(R1.text)

    R2 = S.getpage("zonedata/devices", params={"filter.zone.id": "4"})
    print(R2.headers)
    print(R2.text)

    R3 = S.get("zonedata/devices", params={"filter.zone.id": "4"})
    count = 0
    for d in R3:
        count += 1
        print("%d %s" % (count, d['mac']))
    print("Total count of devices: %d" % count)

    for size in (1, 5, 500):
        s = APIKeyServer(
            "i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlI" +
            "joxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMn" +
            "sdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds", page_size=size)

        r4 = s.get("zonedata/devices", params={"filter.zone.id": "4"})
        count = 0
        for d in r4:
            count += 1
        print("Page size: %d, Count: %d" % (size, count))
