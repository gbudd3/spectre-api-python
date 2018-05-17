'''This module carries the code needed to deal with Spectre collectors
'''
import ipaddress
from spectreapi import spectre

class Collector:
    '''This class encapsulates operations on Spectre collectors.
    a "Collector" is a set of scan configuration associated with a specific
    Scout network interface.'''
    def __init__(self, id_num, uuid, name, zone, server=None):
        self.id_num = id_num
        self.uuid = uuid
        self.name = name
        self.zone = zone
        self.server = server

    def __repr__(self):
        return('Collector(%d, "%s", "%s", %s)' %
               (self.id_num, self.uuid, self.name, self.zone.__repr__()))

    def __str__(self):
        return('id=%d, uuid=%s, name=%s, zone=%s)' %
               (self.id_num, self.uuid, self.name, self.zone.__str__()))

    def _getCidrs(self, cidr_type):
        if cidr_type not in ('target', 'avoid', 'stop'):
            raise spectre.InvalidArgument('%s is not a valid type for _getCidrs')

        if self.server is None:
            raise spectre.NoServerException('Collector.getCidrs() needs a Collector with a server')

        cidrs = []
        cidr_results = self.server.get('zone/collector/%d/cidr/%s' % (self.id_num, cidr_type))
        for cidr in cidr_results:
            cidrs.append(ipaddress.ip_network(cidr))

        return cidrs

    def _setCidrs(self, cidr_type, *cidrs, append=False):
        if cidr_type not in ('target', 'avoid', 'stop'):
            raise spectre.InvalidArgument('%s is not a valid type for _setCidrs')

        if self.server is None:
            raise spectre.NoServerException('Collector.setCidrs() needs a Collector with a server')

        clist = []
        for cidr in cidrs:
            clist.append('{"address":"%s"}' % str(cidr))
        data = '{"addresses":[' + ','.join(clist) + ']}'
        params = {"append": str(append).lower()}

        results = self.server.post('zone/collector/%d/cidr/%s' %
                                   (self.id_num, cidr_type), data=data, params=params)
        if results.ok:
            return results

        raise spectre.SpectreException(results.text)

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
        Gets the "Target" CIDRs for this collector

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
        '''Return the list of "Avoid" CIDRs for this collector'''
        return self._getCidrs('avoid')

    def getStopCidrs(self):
        '''Return the list of "Stop" CIDRs for this collector'''
        return self._getCidrs('stop')
