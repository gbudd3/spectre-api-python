


16:19 Sun 22-Apr-18 EDT
There are 3 ways to authenticate for API access:

1) API Key
2) Username / Password
3) Client side cert

This library should eventally accommodate all 3
but we'll start with API key.

It's worth thinking about how we'll accommodate
testing without an actual Spectre system handy

for #1, it's something like:

curl -k -H "Authorization: Bearer
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoxNTAxODY1ND
k5Nzc3LCJ1c2VyIjoiYWRtaW4ifQ.FfXNebHCkskwbR3dGfB71c2xHtGaK3
krar8AXI3vWIk" https://192.168.9.186/api/rest/
16:45 Sun 22-Apr-18 EDT
i3 Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMnsdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds

Get your API key through "user key new <username>" at the CLI


17:11 Sun 22-Apr-18 EDT
r=requests.get("https://i3/api/rest/system/information",verify=False,headers={'Authorization':"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoxNTI0NDI5ODU2NTA2LCJ1c2VyIjoiYWRtaW4ifQ.KEaRBjPVMnsdPAG6l3oinHOjPFAfsfUkgOs0YKyhwds", 'Accept':'json;pretty'})

>>> print(r.text)
{
  "@class" : "apiresponse",
  "status" : "SUCCESS",
  "method" : "SystemManagement.getSystemInformation",
  "results" : [ {
    "@class" : "systeminformation",
    "name" : "i3",
    "uuid" : "420EF9B6-FEE7-B3C7-C454-3965CC461604",
    "version" : "3.3.0.11241",
    "osversion" : "Linux 2.6.32-696.20.1.el6.x86_64",
    "systemType" : "COMMANDER"
  } ]
}
