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

HOST            = "localhost"
PORT            = 8080
INVALID_PATH    = "INVALID_PATH"
INVALID         = "INVALID"
REDIRECT        = "REDIRECT"

HTML_200    = "HTTP/1.1 200 OK\r\nContent-type:text/html;charset=utf8\r\n\r\n"
HTML_301    = "HTTP/1.1 301 Moved Permanently\r\nLocation: "
HTML_404    = "HTTP/1.1 404 Not Found\r\nContent-type:text/html;charset=utf8\r\n\r\n<html><body><h2>404 Not Found</h2></body></html>"
CSS_200     = "HTTP/1.1 200 OK\r\nContent-type:text/css;charset=utf8\r\n\r\n"
ICO_200     = "HTTP/1.1 200 OK\r\nContent-type:image/x-icon;charset=utf8\r\n\r\n"
HEADER_END  = "\r\n\r\n"

class ResponseBuilder:

    def create200_HTML(self, payload):
        return HTML_200 + payload

    def create200_CSS(self, payload):
        return CSS_200 + payload

    def create200_ICO(self, payload):
        return ICO_200 + payload

    def create404(self):
        return HTML_404

    def create301(self, payload):
        redirection = HTML_301 + "http://" + HOST + ":" + str(PORT) + payload + HEADER_END
        return redirection

# Parses the request and returns different parts such as the requested
# path and mime type
# Includes methods to build a valid response based on the supplied request
class RequestHandler:

    def isFile(self, fileName):
        if (path.endswithignorecase('.html') or
            path.endswith('.css') or
            path.endswith('.ico')):
            return True
        else:
            return false

    # This method takes into account input such as www/../../../ .. /index.html
    # It will remove the ../ sequences as appropriate and allow for access to the 
    # www/ path only
    def sanitizePath(self, rawPath):
        
        directoryStack = []                 # stack containing path structure
        rawPath = rawPath.strip(' \t\n\r')
        directories = filter(None, rawPath.split('/'))    # get each directory seperately

        for dir in directories:
            if dir == '..':
                if len(directoryStack) == 0:
                    return INVALID_PATH
                else:
                    directoryStack.pop()
            else:
                directoryStack.append(dir)

        if len(directoryStack) == 0:
            return "www/"

        cleanPath = "www"
        for dir in directoryStack:
            cleanPath += "/"
            cleanPath += dir

        return cleanPath
        
    def serveResource(self, path, mimeType):
        rb = ResponseBuilder()

        if mimeType == REDIRECT:
            return rb.create301(path + "/")

        # if invalid path or file doesn't exist, return a 404 message
        if not os.path.isfile(path):
            return rb.create404()

        stream = self.readFile(path)
        if mimeType == 'html':
            return rb.create200_HTML(stream)
        if mimeType == 'css':
            return rb.create200_CSS(stream)
        if mimeType == 'ico':
            return rb.create200_ICO(stream)
        if mimeType == INVALID:
            return rb.create404()

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

        path = request.split( )[1]  # this is the full path

        if path.endswith('/'):
            # no redirection required, clean the path and return
            cleanPath = self.sanitizePath(path)
            if (cleanPath == INVALID_PATH):
                return self.serveResource(cleanPath, INVALID)
            else:
                cleanPath += '/index.html'
                return self.serveResource(cleanPath, 'html')

        elif path.endswith('.html'):
            # no redirection required, clean the path and return the requested html file
            cleanPath = self.sanitizePath(path)
            if (cleanPath == INVALID_PATH):
                return self.serveResource(cleanPath, INVALID)
            else:
                return self.serveResource(cleanPath, 'html')

        elif path.endswith('.css'):
            # no redirection required, clean the path and return the requested css file
            cleanPath = self.sanitizePath(path)
            if (cleanPath == INVALID_PATH):
                return self.serveResource(cleanPath, INVALID)
            else:
                return self.serveResource(cleanPath, 'css')

        elif path.endswith('.ico'):
            # no redirection required, clean the path and return the requested ico file
            cleanPath = self.sanitizePath(path)
            if (cleanPath == INVALID_PATH):
                return self.serveResource(cleanPath, INVALID)
            else:
                return self.serveResource(cleanPath, 'ico')

        else: 
            # redirection required, no trailing slash or valid filetype being requested
            return self.serveResource(path, REDIRECT)
        

# Server class that handles the web requests
# Supplies requests to a RequestHandler instance to create appropriate 
# responses for each request. These responses are then served back to the client
class MyWebServer(SocketServer.BaseRequestHandler):

    # Handle requests
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

         # Instance to create responses for all requests
        rh = RequestHandler()
        
        # build a response for the supplied request
        response = rh.buildResponse(self.data)

        # serve the response
        self.request.sendall(response)

# Init server
if __name__ == "__main__":
    SocketServer.TCPServer.allow_reuse_address = True
    
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
