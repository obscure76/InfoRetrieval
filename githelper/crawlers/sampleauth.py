import json
from restkit import Resource, BasicAuth, Connection, request
from socketpool import ConnectionPool
import getpass
 
pool = ConnectionPool(factory=Connection)
serverurl="https://api.github.com"
print 'Enter your username:'
username = raw_input()
password = getpass.getpass("Enter your password here:") 
# Add your username and password here, or prompt for them
auth=BasicAuth(username, password)
 
# Use your basic auth to request a token
# This is just an example from http://developer.github.com/v3/
authreqdata = { "scopes": [ "public_repo" ], "note": "admin script" }
resource = Resource('https://api.github.com/authorizations', pool=pool, filters=[auth])
response = resource.post(headers={ "Content-Type": "application/json" }, payload=json.dumps(authreqdata))
token = json.loads(response.body_string())['token']
"""
Once you have a token, you can pass that in the Authorization header
You can store this in a cache and throw away the user/password
This is just an example query.  See http://developer.github.com/v3/ 
for more about the url structure
"""
#token = '94038d59a46c5ea1aa4f11626a83cde3e8794668' 
resource = Resource('https://api.github.com/user/repos', pool=pool)
headers = {'Content-Type' : 'application/json' }
headers['Authorization'] = 'token %s' % token
response = resource.get(headers = headers)
repos = json.loads(response.body_string())
for each in repos:
    print each['clone_url']
