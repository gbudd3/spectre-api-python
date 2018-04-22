

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
