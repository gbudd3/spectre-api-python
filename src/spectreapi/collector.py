import ipaddress

class Collector:
    def __init__(self, id, uuid, name, zone, server=None):
        self.id = id
        self.uuid = uuid
        self.name = name
        self.zone = zone
        self.server = server

    def __repr__(self):
        return('Collector(%d, "%s", "%s", %s)' % (self.id, self.uuid, self.name, self.zone.__repr__()))

    def __str__(self):
        return('id=%d, uuid=%s, name=%s, zone=%s)' % (self.id, self.uuid, self.name, self.zone.__str__()))

    def _getCidrs(self, type):
        if type not in ('target', 'avoid','stop'):
            raise InvalidArgument('%s is not a valid type for _getCidrs')

        if self.server is None:
            raise NoServerException('Collector.getCidrs() requires a Collector with a server')

        cidrs = []
        r = self.server.get('zone/collector/%d/cidr/%s' % (self.id, type))
        for c in r:
            cidrs.append(ipaddress.ip_network(c))

        return cidrs

    def _setCidrs(self, type, *cidrs, append=False):
        if type not in ('target', 'avoid','stop'):
            raise InvalidArgument('%s is not a valid type for _setCidrs')

        if self.server is None:
            raise NoServerException('Collector.getCidrs() requires a Collector with a server')

        clist = []
        for cidr in cidrs:
            clist.append('{"address":"%s"}' % str(cidr))
        data = '{"addresses":[' + ','.join(clist) + ']}'
        params = { "append": str(append).lower() }

        r = self.server.post('zone/collector/%d/cidr/%s' % (self.id, type), data=data, params=params)
        if r.ok:
            return r
        
        raise SpectreException(r.text)

    def setTargetCidrs(self, *cidrs, append=False):
        ''' Sets Targets for a given Collector.
        By default it will overwrite all targets for this collector, set append=True
        to add CIDRs to the target list.
        >>> import spectreapi
        >>> server = spectreapi.UsernameServer('6hour','admin','admin')
        >>> collector = server.getCollectorByName('RodSerling')
        >>> collector.getTargetCidrs() # doctest: +ELLIPSIS
        [IPv4Network(...
        >>> collector.setTargetCidrs('10.0.0.1/32','10.0.0.2/32',append=True)
        <Response [200]>
        >>> collector.getTargetCidrs() # doctest: +ELLIPSIS
        [IPv4Network(...
        >>>
        '''
        return self._setCidrs('target', *cidrs, append=append)

    def setAvoidCidrs(self, *cidrs, append=False):
        '''Set "Avoid" CIDRs, Spectre shouldn't emit packets
        at these addresses (though we could trace through them
        via path as we're not targeting the hops themselves)'''
        return self._setCidrs('avoid', *cidrs, append=append)

    def setStopCidrs(self, *cidrs, append=False):
        '''Set "Stop" CIDRs, if Spectre sees a hop in one of 
        these CIDRs it should stop tracing that path'''
        return self._setCidrs('stop', *cidrs, append=append)

    def getTargetCidrs(self):
        '''
        >>> import spectreapi
        >>> s = spectreapi.UsernameServer('6hour','admin','admin')
        >>> c = s.getCollectors()[0]
        >>> c.name
        'RodSerling'
        >>> c.getTargetCidrs() # doctest: +ELLIPSIS
        [IPv4Network(...
        >>>
        '''
        return self._getCidrs('target')

    def getAvoidCidrs(self):
        return self._getCidrs('avoid')

    def getStopCidrs(self):
        return self._getCidrs('stop')


