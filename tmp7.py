import httplib, urllib
params = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
#headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
conn = httplib.HTTPConnection("localhost:8000")
conn.request("POST", "", params, headers)
response = conn.getresponse()
print response.status, response.reason
data = response.read()
conn.close()
