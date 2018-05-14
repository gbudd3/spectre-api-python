import ipaddress
from distutils.version import LooseVersion

class Zone:
    def __init__(self, id, name, description=None, server=None):
        self.id = id
        self.name = name
        self.description = description
        self.server = server

    def __repr__(self):
        return('Zone(%d, "%s", "%s")' % (self.id, self.name, self.description))

    def __str__(self):
        return('id=%d, name=%s, description=%s)' % (self.id, self.name, self.description))

    def _getCidrs(self, type):
        if type not in ('known', 'trusted','internal'):
            raise InvalidArgument('%s is not a valid type for _getCidrs')

        if self.server is None:
            raise NoServerException('Collector.getCidrs() requires a Collector with a server')

        cidrs = []
        r = self.server.get('zone/%d/cidr/%s' % (self.id, type))
        for c in r:
            cidrs.append(ipaddress.ip_network(c))

        return cidrs

    def getKnownCidrs(self):
        return self._getCidrs('known')

    def getEligibleCidrs(self):
        '''For reasons lost in the dim reaches of time the system
        calls "Eligible" as "Trusted" under the covers'''
        return self._getCidrs('trusted')

    def getTrustedCidrs(self):
        '''For reasons lost in the dim reaches of time the system
        calls "Eligible" as "Trusted" under the covers'''
        return self._getCidrs('trusted')

    def getInternalCidrs(self):
        return self._getCidrs('internal')

    def _setCidrs(self, type, *cidrs, append=False):
        if type not in ('known', 'trusted','internal'):
            raise InvalidArgument('%s is not a valid type for _setCidrs')

        if self.server is None:
            raise NoServerException('Collector.setCidrs() requires a Zone with a server')

        clist = []
        print(cidrs)
        for cidr in cidrs:
            clist.append('{"address":"%s"}' % str(cidr))
        data = '{"addresses":[' + ','.join(clist) + ']}' 
        params = { "append": str(append).lower() }

        r = self.server.post('zone/%d/cidr/%s' % (self.id, type), data=data, params=params)
        if r.ok:
            return r
        
        raise SpectreException(r.text)

    def setKnownCidrs(self, *cidrs, append=False):
        return self._setCidrs('known', *cidrs, append=append)

    def setEligibleCidrs(self, *cidrs, append=False):
        return self._setCidrs('trusted', *cidrs, append=append)

    def setTrustedCidrs(self, *cidrs, append=False):
        return self._setCidrs('trusted', *cidrs, append=append)

    def setInternalCidrs(self, *cidrs, append=False):
        return self._setCidrs('internal', *cidrs, append=append)


    def getDeviceDetailsByIP(self,ip):
        '''Return the device(s) for a zone with an address of <ip>'''
        params = {
                'filter.zone.id': self.id,
                'filter.address.ip' : ip,
                'detail.ScanType' : True,
                'detail.Attributes' : True,
                'detail.Protocol' : True,
                'detail.Port' : True,
                'detail.AlternateAddress' : True,
                #'detail.Profile' : True,
                #'detail.ProfileDetails' : True,
                'detail.ReferenceIp' : True,
                'detail.Details' : True,
                'detail.LeakResponse' : True,
                'detail.Certificate' : True,
                'detail.Interfaces' : True,
                'detail.Vlans' : True,
                'detail.Collector' : True,
            }

        if LooseVersion(self.server.version) >= LooseVersion("3.3.1"):
            params['detail.Profile'] = True
            params['detail.ProfileDetails'] = True
        
        return self.server.get('zonedata/devices',params=params)

