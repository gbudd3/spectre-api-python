"""This module carries the code needed to deal with Spectre collectors
"""
import calendar
import ipaddress
import json
import math
import time
from typing import List, Union

import spectreapi

IPNetwork = Union[ipaddress.IPv4Network, ipaddress.IPv6Network]


class Collector:
    """This class encapsulates operations on Spectre collectors.
    a "Collector" is a set of scan configuration associated with a specific
    Scout network interface."""

    def __init__(self, id_num, uuid, name, zone, server=None):
        self.id_num = id_num
        self.uuid = uuid
        self.name = name
        self.zone = zone
        self.server = server

    def __repr__(self):
        return f'Collector({self.id_num}, "{self.uuid}", "{self.name}", {self.zone.__repr__()}'

    def __str__(self):
        return f'id={self.id_num}, uuid={self.uuid}, name={self.name}, zone={self.zone.__str__()})'

    def _get_cidrs(self, cidr_type) -> List[IPNetwork]:
        if cidr_type not in ('target', 'avoid', 'stop'):
            raise spectreapi.InvalidArgument(f'{cidr_type} is not a valid type for _get_cidrs')

        if self.server is None:
            raise spectreapi.NoServerException('Collector.getCidrs() needs a Collector with server')

        cidrs = []
        cidr_results = self.server.get(f'zone/collector/{self.id_num}/cidr/{cidr_type}')
        for cidr in cidr_results:
            cidrs.append(ipaddress.ip_network(cidr))

        return cidrs

    def _set_cidrs(self, cidr_type, *cidrs, append=False, chunk_size=5000):
        if cidr_type not in ('target', 'avoid', 'stop'):
            raise spectreapi.InvalidArgument('%s is not a valid type for _set_cidrs')

        if self.server is None:
            raise spectreapi.NoServerException('collector.setcidrs() needs a collector with server')

        clist = []
        results = None
        for cidr in cidrs:
            if isinstance(cidr, list):  # okay, we're a list of cidrs (hopefully)
                for c in cidr:
                    clist.append(f'{{"address":"{c}"}}')
            else:
                clist.append(f'{{"address":"{str(cidr)}"}}')

        for i in range(math.ceil(len(clist) / chunk_size)):
            data = '{"addresses":[' + ','.join(clist[i * chunk_size:(i + 1) * chunk_size]) + ']}'
            params = {"append": str(append).lower()}
            results = self.server.post(f'zone/collector/{self.id_num}/cidr/{cidr_type}',
                                       data=data, params=params)
            append = True  # after the first chunk, append regardless

            if not results.ok:
                raise spectreapi.SpectreException(results.text)

        return results

    def _delete_cidrs(self, cidr_type, *cidrs, chunk_size=5000):
        if cidr_type not in ('target', 'avoid', 'stop'):
            raise spectreapi.InvalidArgument('%s is not a valid type for _delete_cidrs')

        if self.server is None:
            raise spectreapi.NoServerException('collector._delete_cidrs() needs a server')

        clist = []
        results = None
        for cidr in cidrs:
            if isinstance(cidr, list):  # okay, we're a list of cidrs (hopefully)
                for c in cidr:
                    clist.append(f'{{"address":"{c}"}}')
            else:
                clist.append(f'{{"address":"{str(cidr)}"}}')

        for i in range(math.ceil(len(clist) / chunk_size)):
            data = '{"addresses":[' + ','.join(clist[i * chunk_size:(i + 1) * chunk_size]) + ']}'
            results = self.server.delete(f'zone/collector/{self.id_num}/cidr/{cidr_type}',
                                         data=data)
            if not results.ok:
                raise spectreapi.SpectreException(results.text)

        return results

    def delete_avoid_cidrs(self, *cidrs, chunk_size=5000):
        return self._delete_cidrs('avoid', *cidrs, chunk_size=chunk_size)

    def delete_target_cidrs(self, *cidrs, chunk_size=5000):
        return self._delete_cidrs('target', *cidrs, chunk_size=chunk_size)

    def delete_stop_cidrs(self, *cidrs, chunk_size=5000):
        return self._delete_cidrs('stop', *cidrs, chunk_size=chunk_size)

    def set_target_cidrs(self, *cidrs, append=False, chunk_size=5000):
        """ Sets Targets for a given Collector.
        By default it will overwrite all targets for this collector, set append=True
        to add CIDRs to the target list.

        >>> import spectreapi
        >>> server = spectreapi.UsernameServer('server','username','password')
        >>> collector = server.getCollectorByName('RodSerling')
        >>> collector.get_target_cidrs() # doctest: +ELLIPSIS
        [IPv4Network(...
        >>> collector.set_target_cidrs('10.0.0.1/32','10.0.0.2/32',append=True)
        <Response [200]>
        >>> collector.get_target_cidrs() # doctest: +ELLIPSIS
        [IPv4Network(...
        >>>
        """
        return self._set_cidrs('target', *cidrs, append=append, chunk_size=chunk_size)

    def set_avoid_cidrs(self, *cidrs, append=False, chunk_size=5000):
        """Set "Avoid" CIDRs, Spectre shouldn't emit packets
        at these addresses (though we could trace through them
        via path as we're not targeting the hops themselves)"""
        return self._set_cidrs('avoid', *cidrs, append=append, chunk_size=chunk_size)

    def set_stop_cidrs(self, *cidrs, append=False, chunk_size=5000):
        """Set "Stop" CIDRs, if Spectre sees a hop in one of
        these CIDRs it should stop tracing that path"""
        return self._set_cidrs('stop', *cidrs, append=append, chunk_size=chunk_size)

    def get_target_cidrs(self) -> List[IPNetwork]:
        """
        Gets the "Target" CIDRs for this collector

        >>> import spectreapi
        >>> s = spectreapi.UsernameServer('server','username','password')
        >>> c = s.getCollectors()[0]
        >>> c.name
        'RodSerling'
        >>> c.get_target_cidrs() # doctest: +ELLIPSIS
        [IPv4Network(...
        >>>
        """
        return self._get_cidrs('target')

    def get_avoid_cidrs(self) -> List[IPNetwork]:
        """Return the list of "Avoid" CIDRs for this collector"""
        return self._get_cidrs('avoid')

    def get_stop_cidrs(self) -> List[IPNetwork]:
        """Return the list of "Stop" CIDRs for this collector"""
        return self._get_cidrs('stop')

    def add_traces(self, traces, scanType='external', protocol='unspecified'):
        if "traces" not in traces:
            traces = {'traces': [traces]}

        responses = {'collector': {'id': self.id_num, 'uuid': self.uuid},
                     'scanType': scanType,
                     'protocol': protocol,
                     'time': calendar.timegm(time.gmtime()) * 1000,
                     'NACK': False
                     }

        for trace in traces['traces']:
            trace['response'] = responses

        result = self.server.put(f'publish/path/{self.uuid}', data=json.dumps(traces))
        if not result.ok:
            raise spectreapi.APIException(result)

    def add_devices(self, devices, scanType='external', protocol='unspecified', nack=False):
        if "devices" not in devices:
            devices = {'devices': [devices]}

        responses = [{'collector': {'id': self.id_num, 'uuid': self.uuid},
                      'scanType': scanType,
                      'protocol': protocol,
                      'time': calendar.timegm(time.gmtime()) * 1000,
                      'NACK': nack}]

        for device in devices['devices']:
            device['responses'] = responses

        result = self.server.put(f'publish/device/{self.uuid}', data=json.dumps(devices))
        if not result.ok:
            raise spectreapi.APIException(result)

    def get_property(self, prop):
        if self.server is None:
            raise spectreapi.NoServerException('Collector.get_property() needs a server')

        results = self.server.get(f'zone/collector/{self.id_num}/property/get/{prop}')
        if not results.ok:
            raise spectreapi.APIException(results)

        return json.loads(results.results.text).get('result')

    def set_property(self, prop, value, *, query_first=True):
        if self.server is None:
            raise spectreapi.NoServerException('Collector.set_property() needs a server')

        if query_first and self.get_property(prop) == value:
            return

        results = self.server.get(f'zone/collector/{self.id_num}/property/set/{prop}',
                                  params={'value': value})
        if not results.ok:
            raise spectreapi.APIException(results)

    def get_config(self):
        if self.server is None:
            raise spectreapi.NoServerException(
                'Collector.get_property() needs a server')

        results = self.server.get('/zone/collector',
                                  params={'detail.Config': True,
                                          'detail.Interface': True,
                                          'filter.collector.id': self.id_num})
        return json.loads(results.results.text).get('results')[0]
