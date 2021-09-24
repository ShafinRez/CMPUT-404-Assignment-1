#  coding: utf-8 
import socketserver 
import os
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


class MyWebServer(socketserver.BaseRequestHandler):
    
    def go(self,link):
        dir = 'www'
        if '.html' in link:
            content_type = 'text/html'
        elif '.css' in link:
            content_type = 'text/css'
        else: 
            content_type = 'text/plain'

        if os.path.exists(dir + link):
            path = dir + link + 'index.html'
            
            self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n Content Type:'+ content_type, 'utf-8'))
            html =  open(path, 'rb')
            html = html.read()
            self.request.sendall(html)
        
        elif os.path.exists(dir+link + '/'):
            
            self.request.sendall(bytearray('HTTP/1.1 301 Moved Permanently\r\n', 'utf-8'))
    
    
        else:
           self.request.sendall(bytearray('HTTP/1.1 404 Page Not Found\r\n', 'utf-8')) 

    def handle(self):
        self.data = self.request.recv(1024).strip()
        decode = self.data.decode('utf-8')
        d = decode.split()
        cmd = d[0]
        link = d[1]
       
    
        if cmd == 'GET':
            self.go(link)
        else:
            self.request.sendall(bytearray('HTTP/1,1 405 Not Allowed\r\n', 'utf-8'))
        

        print ("Got a request of: %s\n" % self.data)
        self.request.sendall(bytearray("OK",'utf-8'))
	
	
	
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
   
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()