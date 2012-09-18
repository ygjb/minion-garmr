minion-garmr
============

plugin service, plugin spec, and garmr plugin for minion


plugin-service.py - Bottle based REST API that wraps a MinionPlugin object.

plugin.py - helper functions and the MinionPlugin abstract class

ShellPlugin.py - MinionPlugin that implements features for managing command line based tools

GarmrPlugin.py - Implementation of ShellPlugin that manages Garmr