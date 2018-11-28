# import os and sys for find the files outside the current folder
import os
import sys
# pyjsonrpc as the backend server
import pyjsonrpc

# translate bson to string -> then string to json (since data stored in mongodb as bson format)
import json
from bson.json_util import dumps

# import mongodb_client for db connection/read/write
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client

SERVER_HOST = 'localhost'
SERVER_PORT = 4040
PROPERTY_TABLE_NAME = 'properties'

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """Test method"""
    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        print "add gets called with %d and %d" % (a, b)
        return a + b

    """First method used to take user input of zipcode or cityname"""
    @pyjsonrpc.rpcmethod
    def searchArea(self, query):
    	res = []
    	# if query is pure digits, user's input is zipcode, query the database
    	if query.isdigit():
    		db = mongodb_client.getDB()
    		res = db[PROPERTY_TABLE_NAME].find({'zipcode':query})
    		res = json.loads(dumps(res))

    	# if not pure digits, user's input is cityname
    	# input format should be "city, state"
    	else:
    		city = query.split(',')[0].strip()
    		state = query.split(',')[1].strip()
    		# TODO: search DB
    	return res



http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print "Starting HTTP server..."
print "Listening on %s:%d" % (SERVER_HOST, SERVER_PORT)

http_server.serve_forever()
