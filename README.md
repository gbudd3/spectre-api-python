# spectre-api-python

## General
This module is intended to make it a bit easier to work with
The Lumeta Corporation's Spectre API.

Lumeta and Spectre are both registered trademarks of the Lumeta Corporation

Install this module by running `pip3 install spectre-api`

### Introduction
This Python module is intended to be a relatively light weight wrapper around the Spectre API.
The idea is to abstract out some of the authentication and paging pieces to make it easier to
focus on fine-tuning the actual underlying calls.  Basically, you configure a server
(currently using username/password or API Key authentication) and then have it perform API calls.
For example:
```python
>>> import spectreapi
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
A **Server** is the base class that has most of the functionality
needed to use the Spectre API.  You'll instantiate a more specific
**Server** based on which authentication method you're using.

### UsernameServer
`spectreapi.UsernameServer(<server>, <username>, <password>, [<page_size>,] [<verify>])`
Where:

`<server>` = The IP address or DNS name of the Spectre Command Center 

`<username>` = Username

`<password>` = Password 

`<page_size>` = How many results should a GET request return at a time.

`<verify>` = Should we verify the SSL certificate of the server (True or False, defaults to False).  You'll want to leave this a False unless you've given your command center an actual SSL certificate.



Behind the scenes, this makes an API call to `system/information` with basic authentication
(over https) and then uses the resulting JSESSIONID cookie for the rest of the time.

### APIKeyServer
`spectreapi.APIKeyServer(<server>, <api_key>, [, <page_size>] [, <verify>])`
Where:

`<server>` = The IP address or DNS name of the Spectre Command Center 

`<api_key>` = API Key for API access.  You get this via the GUI or by issuing the
`user key new <username>` command at the command center CLI.

`<page_size>` = How many results should a GET request return at a time.

`<verify>` = Should we verify the SSL certificate of the server (True or False, defaults to False).  You'll want to leave this a False unless you've given your command center an actual SSL certificate.



## GET, POST, PUT, DELETE

## Notes on using the underlying Spectre API

