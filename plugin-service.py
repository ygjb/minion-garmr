
from bottle import abort, get, put, post, delete, request, run
import json
import os
import plugin
from GarmrPlugin import GarmrPlugin

keys = { 
 "64c4c469ab0743a368d00466e1eb8608" : 
 { 
  "acl" :
   {
    "admin" : True, 
    "api" : True
   }, 
  "owner" : "Bob"
 }, 

 "ca8601b9a687c34703e46328e3dc69eb" : 
 { 
  "acl" :
   {
    "admin" : False, 
    "api" : True
   }, 
  "owner" : "Alice"
 }  
}

sessions = {}

plugin = GarmrPlugin

# ==== Handle REST API ====

def authorized_for(req, feature):
 key = req.headers.get('Authorization')
 # XX - timing independent check of key strings is required.
 return (key in keys) and ("acl" in keys[key]) and (feature in keys[key]["acl"]) and (keys[key]["acl"][feature] == True)

def gen_session_key():
 return ''.join('%02x' % ord(x) for x in os.urandom(16))

def do_create_session(key, name):
 if (not authorized_for(request, "api")):
  abort(401, "Unauthorized request")

 session = gen_session_key();
 while (session in sessions):
  session = gen_session_key()
 sessions[session] = { "name" : name, "configuration" : "", "plugin" : plugin(), "owner" : request.headers.get('Authorization') }
 return { "session" : session, "Message" : "Created new session named '%s'" % name }

# ==== Handle REST API ====

@get("/sessions")
def get_sessions():
 #'''GET - get a list of active sessions (permission based)'''
 if (not authorized_for(request, "api")):
  abort(401, "Unauthorized request.")
 key = request.headers.get('Authorization')
 s = {}
 for session in sessions:
  if (sessions[session]["owner"] == key):
   s[session] = { 
    "name" : sessions[session]["name"],
    "owner" : keys[sessions[session]["owner"]]["owner"]
   }
 return { 'sessions' : s }

@put("/session/create/<name>")
def create_session(name = None):
 if (name == None):
  abort(500, "Cannot create a session without a name.")
 return do_create_session(request, name)

@delete("/session/<session>")
def terminate_session():
  if (not is_admin(request)):
    abort(401, "Unauthorized request.")
  if (not session in sessions):
    abort(404, "Invalid session.")

  '''DELETE - terminate a session'''
  abort(501, "Terminating the session is not yet supported.")

# Interrogate the service for default values
@get("/default/configure")
def get_default():
  if (not authorized_for(request, "api")):
    abort(401, "Unauthorized request.")
  return plugin.default

@get("/default/configure/<setting>")
def get_default(setting = None):
  '''GET - retrieve the configuration'''
  abort(501, "Getting a default configuration settingis not yet implemented.") 

# Configure entire session
@get("/session/<session>/configure")
def get_configuration(session = None):
  '''GET - retrieve the configuration'''
  abort(501, "Getting the configuration is not yet implemented.") 

@put("/session/<session>/configure")
def set_configuration(session = None):
  '''PUT - overwrite the configuration with values supplied'''
  abort(501, "Setting the entire configuration is not yet implemented.") 

@delete("/session/<session>/configure")
def clear_configuration(session = None):
  '''DELETE - Reset the configuration to the default'''
  abort(501, "Clearing the configuration is not yet implemented.") 

# Configure individual values
@get("/session/<session>/configure/<setting>")
def get_value(session = None, setting = None):
  ''' GET - get the value of the element ''' 
  abort(501, "Getting the value of '%s' on session '%s' is not yet implemented." % (session, setting)) 

@put("/session/<session>/configure/<setting>")
def set_value(session = None, setting = None):
  ''' PUT - set the value of the element '''
  abort(501, "Setting a value is not yet implemented.") 

@delete("/session/<session>/configure/<setting>")
def clear_value(session = None, setting = None):
  ''' DELETE - set the element to the default value, or delete it, if it is not in the defaults '''
  abort(501, "Clearing a value is not yet implemented.") 

# Query session status
@get("/session/status/<session>")
def session_status(session = None):
  if (authorized_for(request, "api")):
    return sessions[session]["plugin"].status()
  else:
    abort(401, "Not authorized.")

@get("/session/state/<session>")
def session_state(session = None):
  ''' GET - retrieve a set of available state changes [START, SUSPEND, TERMINATE] '''
  abort(501, "Retrieving session status is not yet implemented.")

@put("/session/state/<session>/<state>")
def session_change_state(session = None):
  '''PUT - start a pending session, return an error on runs in any other state'''
  #States: START, SUSPEND, TERMINATE
  abort(501, "Altering a session state is not yet implemented.")

run(host="localhost", port=8090)
