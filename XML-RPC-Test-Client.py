import xmlrpclib

username = 'a'
password = 'b'

# Define The Server
server = xmlrpclib.Server('https://lcsee.wvu.edu/lamp/lcsee-mytime/XML-RPC-Server.py')

# Call The Function
print server.MyTimeMobile(username, password)
