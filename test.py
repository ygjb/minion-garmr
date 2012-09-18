import json
import requests

bob_key = "64c4c469ab0743a368d00466e1eb8608"
alice_key = "ca8601b9a687c34703e46328e3dc69eb"
url = "localhost:8090"

name = "Alice Session"
payload = {}
headers = {'Authorization' : alice_key}
r = requests.put("http://%s/session/create/%s"%(url, name), data=payload, headers=headers)
print r.json

name = "Bob Session"
payload = {}
headers = {'Authorization' : bob_key}
r = requests.put("http://%s/session/create/%s"%(url, name), data=payload, headers=headers)
session_bob = r.json["session"]
print r.json


# Check for Admin Session List
print "Pull list of sessions for Alice (should only see alices session)"
headers = {'Authorization' : alice_key}
r = requests.get("http://%s/sessions" % url, headers=headers)
print r.json

# Check for non-admin Session List
print "Pull list of sessions for Bob, with admin privs (should see both sessions)"
headers = {'Authorization' : bob_key}
r = requests.get("http://%s/sessions" % url, headers=headers)
print r.json

print "Get Default settings."
r = requests.get("http://%s/default/configure" % url, headers = headers)
print r.json

print "Get Default setting."
r = requests.get("http://%s/default/configure/template" % url, headers = headers)
print r.json

print "Check session status!"
r = requests.get("http://%s/session/status/%s" % (url, session_bob), headers = headers)
print r.json
