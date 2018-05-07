# spectre-api-python

## General
This module is intended to make it a bit easier to work with
The Lumeta Corporation's Spectre API.

Lumeta and Spectre are both registered trademarks of the Lumeta Corporation

### Introduction
This Python module is intended to be a relatively light weight wrapper around the Spectre API.
The idea is to abstract out some of the authentication and paging pieces to make it easier to
focus on fine-tuning the actual underlying calls.  Basically, you configure a server
(currently using username/password or API Key authentication) and then have it perform API calls.
For example:
```
>>> s = spectreapi.UsernameServer("cc", "username", "password")
>>> r = s.get("zonedata/devices", params = { "filter.zone.id": 1} )
>>> for d in r:
...     if d['ip'] is not None:
...             print(d['ip'])
...
10.2.1.1
10.201.0.1
10.201.0.7
10.202.0.1
10.202.0.2
172.18.1.180
>>>
```
## Servers

## GET, POST, PUT, DELETE

## Notes on using the underlying Spectre API

