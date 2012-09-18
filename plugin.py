from copy import deepcopy

def hasKey(collection, key):
 path = key.strip().split('.')
 ptr = collection
 keyCheck = path[-1]
 while (path[0] in ptr):
  if ((path[0] == keyCheck) and (len(path) == 1)):
    return ptr[path[0]]
  ptr = ptr[path[0]]
  path.pop(0) 
 raise Exception("Value not found in collection.")

def setKey(collection, key, value, force = False):
 path = key.strip().split('.')
 ptr = collection
 keyCheck = path[-1]
 if (force):
    if (not path[0] in ptr):
        ptr[path[0]] = {}
 while (path[0] in ptr):
  if ((path[0] == keyCheck) and (len(path) == 1)):
    ptr[path[0]] = value
    return
  ptr = ptr[path[0]]
  path.pop(0)
  if (force):
    if (not path[0] in ptr):
        ptr[path[0]] = {}
 raise Exception("Path not found")


class MinionPlugin:

    STATUSES = ["PENDING", "WAITING", "RUNNING", "COMPLETE", "CANCELLED", "FAILED"]
    STATES = ["RESUME", "START", "SUSPEND", "TERMINATE"]

    def create_status(self, success, message, status):
        return { "success" : success, "message" : message, "status" : status} 

    default = { }
    def __init__(self, default):
        self.configuration = deepcopy(self.__class__.default)


    def resetConfig(self):
        self.configuration = deepcopy(self.__class__.default)    

    def getConfig(self):
        return self.configuration

    def setConfig(self, config):
        if (self.status()["status"] != "PENDING"):
            raise("Cannot configure a plugin once execution has started.")
        #XXX - Extension Point - do_validate(config), return True|False
        if (self.do_validate(config)):
            self.configuration = config
        else:
            raise ("Invalid configuration exception.")

    def getValue(self, key):
        try:
            return hasKey(self.configuration, key)
        except:
            return None

    def setValue(self, key, value):
        if (self.status()["status"] != "PENDING"):
            raise("Cannot configure a plugin once execution has started.")
        try:
            #XXX - Extension Point do_validate_key(key, value), return True|False
            if (self.do_validate_key(key, value)):
                return setKey(self.configuration, key, value, force)
        except:
            return False


    def status(self):
        try:
            #XXX - Extension Point - do_status(), return create_status()
            result = self.do_status()
            return result
        except:
            return create_status(False, "Plugin was unable to report a status: %s" % sys.exc_info()[0], "FAILED")

    def start(self):        
        try:        
            if (self.canEnterState("START")):
                #XXX - Extension Point - do_start(), return create_status()
                self.do_start()
                query = self.status()
                return create_status(query["success"], "Plugin started: %s" % query["message"], query["status"])
            else:
                return create_status(False, "Plugin could not be started: %s" % query["message"], query["status"])
        except:
            return create_status(False, "START failed: %s" % sys.exc_info()[0], "FAILED")


    def suspend(self):
        try:            
            if (self.canEnterState("SUSPEND")):
                #XXX - Extension Point - do_suspend(), return create_status()
                self.do_suspend()
                query = self.status()
                return create_status(query["success"], "Plugin suspended: %s" % query["message"], query["status"])
            else:
                return create_status(False, "Plugin could not be suspended: %s" % query["message"], query["status"])
        except:
            return create_status(False, "SUSPEND failed: %s" % sys.exc_info()[0], "FAILED")

    def terminate(self):
        try:            
            if (self.canEnterState("TERMINATE")):
                #XXX - Extension Point - do_terminate(), return create_status()
                self.do_terminate()
                query = self.status()
                return create_status(query["success"], "Plugin terminated: %s" % query["message"], query["status"])
            else:
                return create_status(False, "Plugin could not be terminated: %s" % query["message"], query["status"])
        except:
            return create_status(False, "TERMINATE failed: %s" % sys.exc_info()[0], "FAILED")

    def canEnterState(self, state):
        try:
            if not state in STATES:
                raise("%s is not a valid state.")
            #XXX - Extension Point - do_get_states() : return [] containing available states
            states = self.do_get_states()
            return state in states
        except:
            return []

