import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

#I have not a good understanding of what is happening!
class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path != '/style.css':
            print("self.path ist")
            print(self.path)
            self.path = '/index.html'
        try:
            split_path = os.path.splitext(self.path)
            request_extension = split_path[1]
            if request_extension != ".py":
                f = open(self.path[1:]).read()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes(f, 'utf-8'))
            else:
                f = "File not found"
                self.send_error(404,f)
        except:
            f = "File not found"
            self.send_error(404,f)



HOST_NAME = '192.168.178.193'
PORT = 8000

if __name__ == "__main__":
    httpd = HTTPServer((HOST_NAME,PORT),Server)
    print(time.asctime(), "Start Server - %s:%s"%(HOST_NAME,PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(),'Stop Server - %s:%s' %(HOST_NAME,PORT))
