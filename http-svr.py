import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

active = "none"

#I have not a good understanding of what is happening!
class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path != '/some.css':
            
            active = str(self.path)[1:]
            print(active)

            css = f''' 
                body {{background-color: white;}}
                #location:hover {{stroke: #6cf287; stroke-width: 4; fill: #5cf287;}}
                #location {{fill: #f5f5f5;}}
                #ch:hover {{stroke: none; stroke-width: none; fill: #d4d4d4;}}
                #ch {{fill: #f5f5f5;}}
                #{active} {{fill: #5cf287;}}

                @media (prefers-color-scheme: light) {{
                body {{
                    background-color: white;
                    color: black;
                }}
                }}

                @media (prefers-color-scheme: dark) {{
                body {{
                    background-color: black;
                    color: white;
                }}
                }}
             '''



            file = open('/home/pi/Desktop/3.141/some.css', 'w')
            file.write(css)
            file.close()
            
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
