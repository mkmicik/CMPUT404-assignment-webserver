#  coding: utf-8 
import SocketServer
import os.path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

HTML_HEADER     = "HTTP/1.1 200 OK\r\nContent-type:text/html;charset=utf8\r\n\r\n"
CSS_HEADER      = "HTTP/1.1 200 OK\r\nContent-type:text/css;charset=utf8\r\n\r\n"
ICO_HEADER      = "HTTP/1.1 200 OK\r\nContent-type:image/x-icon;charset=utf8\r\n\r\n"
HTML_NOT_FOUND  = "HTTP/1.1 404 Not Found\r\nContent-type:text/html;charset=utf8\r\n\r\n<html><body><h2>404 Not Found</h2></body></html>"

class ResponseBuilder:

    def createResponse(self, payload, mimeType):
        if mimeType == 'html':
            return self.createHTMLResponse(payload)
        if mimeType == 'css':
            return self.createCSSResponse(payload)
        if mimeType == 'ico':
            return self.createICOResponse(payload)

        return self.create404Resonse()

    def createHTMLResponse(self, payload):
        return HTML_HEADER + payload

    def createCSSResponse(self, payload):
        return CSS_HEADER + payload

    def createICOResponse(self, payload):
        return ICO_HEADER + payload

    def create404Resonse(self):
        return HTML_NOT_FOUND

# Parses the request and returns different parts such as the requested
# path and mime type
# Includes methods to build a valid response based on the supplied request
class RequestParser:

    # A naive method that gets the mime type based on the file description
    # in the requested path. eg. .html, .css, .ico
    # TODO: implement a more reliable method of getting the mime type
    def getMimeType(self, path):
        args = path.split('.')
        return args[-1]
        
    # Returns the requested path
    # If the path is invalid, eg. the path does not exist or it requests
    # a file outside of www/, it returns an 'INVALID' flag
    # If the path ends in '/', it will append 'index.html' to the path
    def getPath(self, request):
        # get the path
        args = request.split( )
        path = args[1]      # this should be the path supplied

        # return 404, path not valid
        if path.find('..') != -1:
            return 'INVALID';

        # ends in a '/', we need the index at that directory
        if (path.endswith('/')):
            path += 'index.html'

        # return the full path
        if path.startswith('/'):
            return 'www' + path
        else:
            return 'www/' + path

    # Reads from the requested file and returns the content as
    # a string. Before calling this method, the callee should ensure
    # that the file does in fact exist
    def readFile(self, path):
        file = open(path, 'r')
        stream =  file.read()
        file.close()
        return stream

    # Handles the logic behind creating a valid html respinse based 
    # on the given request
    def buildResponse(self, request):
        path = self.getPath(request)
        mimeType = self.getMimeType(path)
        rb = ResponseBuilder()

        # if invalid path or file doesn't exist, return a 404 message
        if not os.path.isfile(path):
            return rb.create404Resonse()
        # else, we want to create the response using the requested resource
        else: 
            stream = self.readFile(path)
            return rb.createResponse(stream, mimeType)
        
class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        rp = RequestParser()
        self.request.sendall(rp.buildResponse(self.data))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
