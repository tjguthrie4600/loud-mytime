#!/usr/bin/python

import MyTime, SimpleXMLRPCServer, datetime

# Get The Date And Time                                                                   
now = datetime.datetime.now()

# Open The Logs
f = open('/srv/lamp/lcsee-mytime/AccessLog', 'a+')

# Function To Call MyTime Application
def MyTimeMobile(username, password):
    # Make Apache Happy
    print "Content-Type: text/xml\n"
    # Call The Application
    dataStream = MyTime.main([username,password])
    # Write To Logs
    f.write(now.strftime("%Y-%m-%d %H:%M: ") + dataStream + '\n')
    return dataStream

# STAND ALONE SERVER
# ---------------------------------------------------------------------
# Create A Server On Port 8888
#server = SimpleXMLRPCServer.SimpleXMLRPCServer(("10.0.0.11", 8888))
# Register The Functions The Client Can Call
#server.register_function(MyTimeMobile)
# Serve Forever
#server.serve_forever()

# CGI SERVER
# ---------------------------------------------------------------------
# Create A Server
server = SimpleXMLRPCServer.CGIXMLRPCRequestHandler()
# Register The Functions The Client Can Call
server.register_function(MyTimeMobile)
# Handles The Requests
server.handle_request()

# Close The Logs
f.close()
