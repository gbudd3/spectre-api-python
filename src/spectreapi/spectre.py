#!/usr/local/bin/python3
"""
The spectre module is used to make access to Lumeta's Spectre API
a little easier (Lumeta and Spectre are trademarks of the Lumeta Corporation).
"""
import requests
import urllib3
import ipaddress
from spectreapi.zone import Zone
from spectreapi.collector import Collector


class Server():
    """
    A Server is used to make API Calls to a Lumeta Spectre(r) server
    It's not meant to be instantiated directly, use one of its 
    subclasses (e.g. UsernameServer or APIKeyServer) based on how we're
    authenticating to the Spectre Command Center in question.
    """

    def __init__(self, server, page_size=500, verify_cert=False):
        self.session = requests.Session()
        self.session.verify = False
        self.page_size = page_size
        self.url = "https://" + server + "/api/rest/"
        self.host = server
        self.session.timeout = 1
        if verify_cert is False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def close(self):
        '''
        It's not _required_ to close a Server, but if you don't, you might 
        hold tcp sockets open (the underlying requests and urllib3 modules
        hold them for keepalive purposes)
        '''
        self.session.close()

    def post(self, api, **kargs):
        """
        This method POSTs to the Spectre API
        >>> import spectreapi
        >>> s = spectreapi.UsernameServer("6hour", "admin", "admin")
        >>> data = '''
        ...         [{
        ...             "@class":"zone",
        ...             "name":"Twilight",
        ...             "description": "Zone to Test Scanning",
        ...             "organization":{"id":1, "name":"Test Organization"}
        ...         }]
        ...         '''
        >>> r = s.post("zone", data=data)
        >>> r.json()['status']
        'SUCCESS'
        """
        if 'headers' not in kargs:
            kargs['headers'] = {'Accept': 'json:pretty', 'Content-Type': 'application/json'}

        r = self.session.post(self.url + api, **kargs)
        if not r.ok:
            raise APIException(r)
        return r

    def raw_post(self, api, **kargs):
            """
            This method POSTs to the Spectre API but _doesn't_ set any headers.
            This is so we can make things like file uploads work.
            """
            r = self.session.post(self.url + api, **kargs)
            if not r.ok:
                raise APIException(r)
            return r

    def put(self, api, **kargs):
        '''Method PUTs through to the server'''

        if 'headers' not in kargs:
            kargs['headers'] = {'Accept': 'json:pretty', 'Content-Type': 'application/json'}

        r = self.session.put(self.url + api, **kargs)
        if not r.ok:
            raise APIException(r)
        return r


    def delete(self, api, **kargs):

        if 'headers' not in kargs:
            kargs['headers'] = {'Accept': 'json:pretty', 'Content-Type': 'application/json'}

        '''Method DELETEs through to the server'''
        r = self.session.delete(self.url + api, **kargs)
        if not r.ok:
            raise APIException(r)
        return r


    def getpage(self, api, params=None, page=0, headers=None):
        """
        This private method is in place to handle the actual
        fetching of GET API calls
        """
        if params is None:
            params = {"query.pagesize": self.page_size}

        if headers is None:
            headers = {'Accept': 'json:pretty', 'Content-Type': 'application/json'}

        params["query.pagesize"] = self.page_size
        params["query.page"] = page
        results = self.session.get(self.url+api, params=params, timeout=5, headers=headers)
        if not results.ok:
            print(results.text)
            raise APIException(results)
        return results

    def get(self, api, params=None):
        """
        Use this method to GET results from an API call and produce
        an iterable response
        >>> import spectreapi
        >>> s=spectreapi.UsernameServer('6hour','admin','admin')
        >>> s.get('zone').results.json()
        {'@class': 'apiresponse', 'status': 'SUCCESS', 'method': 'ZoneManagement.getZones', 'total': 2, 'results': [{'@class': 'zone', 'id': 2, 'name': 'Twilight', 'description': 'Zone to Test Scanning'}, {'@class': 'zone', 'id': 1, 'name': 'Zone1', 'description': 'Default Zone'}]}
        >>> r = s.get('zone')
        >>> for z in r:
        ...     print(z)
        ...
        {'@class': 'zone', 'id': 2, 'name': 'Twilight', 'description': 'Zone to Test Scanning'}
        {'@class': 'zone', 'id': 1, 'name': 'Zone1', 'description': 'Default Zone'}
        >>>
        """
        return Response(self, api, params)

    def getZones(self):
        '''Returns all the Zones configured on the server'''
        zones = []
        r = self.get('zone')
        for z in r:
            zones.append(Zone(z['id'], z['name'], z['description'], server=self))

        return zones
    
    def getZoneByName(self,name):
        '''Returns the Zone configured on the server named <name> (if present)'''
        zones = []
        r = self.get('zone')
        for z in r:
            if z['name'] == name:
                return Zone(z['id'], z['name'], z['description'], server=self)

        return None



    def getCollectors(self):
        '''Returns the Collectors configured on the server'''
        collectors = []
        r = self.get('zone/collector')
        for c in r:
            collectors.append(Collector(
                c['id'],
                c['uuid'],
                c['name'],
                Zone(c['zone']['id'], c['zone']['name']),
                server=self,
            ))
        return collectors

    def getCollectorByName(self,name):
        '''Returns the Collector configured on the server named <name> (if present)'''
        zones = []
        r = self.get('zone/collector')
        for c in r:
            if c['name'] == name:
                return Collector(
                c['id'],
                c['uuid'],
                c['name'],
                specterapi.Zone(c['zone']['id'], c['zone']['name']),
                server=self,
            )

        return None


class Response():
    """
    This class is used to present the results of a "GET" API call
    It handles iterating through the results and fetching pages as 
    needed from the server
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

    def rewind(self):
        '''Used to reset state after iterating over results'''
        self.page = 0
        self.page_line = 0
        self.results = self.server.getpage(
            self.api, self.params, page=self.page)

    def __iter__(self):
        return self

    def __next__(self):
        '''This facilitates being able to iterate over the results of a GET'''
        if self.page * self.server.page_size + self.page_line == self.total:
            self.rewind()
            raise StopIteration

        if self.page_line < self.server.page_size:
            self.page_line += 1
            try:
                return self.results.json()['results'][self.page_line - 1]
            except IndexError:
                self.rewind()
                raise StopIteration  # This could happen if the underlying query shrinks under us

        else:
            self.page_line = 1
            self.page += 1
            self.results = self.server.getpage(
                self.api, self.params, page=self.page)
            try:
                return self.results.json()['results'][0]
            except IndexError:
                self.rewind()
                raise StopIteration  # This could happen if the underlying query shrinks under us

    def result(self):
        """Return result 0 (the only result for singletons"""
        return self.results.json()['results'][0]

    def values(self):
        """Return the values from the API call"""
        return self.results.json()['results']


class APIKeyServer(Server):
    """
    An APIKeyServer is a Server that uses authentication via API key.
    You get an API key from the CLI via the "user key new <username>" command
    """

    def __init__(self, server, api_key, page_size=500, verify_cert=False):
        """
        APIKeyServer(server,api_key) where
        server is the Spectre server you're connecting to and
        api_key is the API key you've generated

        >>> import spectreapi
        >>> s = APIKeyServer("i3", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"+ \
                ".eyJkYXRlIjoxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMns"+ \
                "dPAG6l3oinHOjPFAfsfUkgOs0YKyhwds")
        >>> r = s.getpage("system/information")
        >>> r.json()['status']
        'SUCCESS'
        >>> r.json()['results'][0]['name']
        'i3'
        """
        super().__init__(server, page_size=page_size,verify_cert=verify_cert)
        self.session.headers['Authorization'] = "Bearer " + api_key

class UsernameServer(Server):
    """
    This Server uses username and password authentication for the initial
    request, and then uses a session cookie from there out
    """
    def __init__(self, server, username, password, page_size=500,verify_cert=False):
        super().__init__(server, page_size=page_size,verify_cert=verify_cert)
        a = requests.auth.HTTPBasicAuth(username, password)
        r = requests.get(self.url + "system/information", verify=False, auth=a)
        self.session.cookies = r.cookies


class SpectreException(Exception):
    pass

class NoServerException(SpectreException):
    pass

class InvalidArgument(SpectreException):
    pass

class APIException(SpectreException):
    def __init__(self,request):
        self.request = request

    def __str__(self):
        return self.request.text

