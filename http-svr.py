import os
from http.server import BaseHTTPRequestHandler, HTTPServer


host_name = '192.168.178.193'    # Change this to your Raspberry Pi IP address
host_port = 8000


class MyServer(BaseHTTPRequestHandler):
    """ A special implementation of BaseHTTPRequestHander for reading data from
        and control GPIO of a Raspberry Pi
    """

    def do_HEAD(self):
        """ do_HEAD() can be tested use curl command 
            'curl -I http://server-ip-address:port' 
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        """ do_GET() can be tested using curl command 
            'curl http://server-ip-address:port' 
        """
        html = '''
            <html>
            <body style="width:960px; margin: 20px auto;">
            <h1>Welcome to my Raspberry Pi</h1>
            <svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
            <g>
             <title>Layer 1</title>
             <path stroke-width="16" d="m255.76723,482.17357c-1.92298,0 -3.84597,0 -5.76895,0c-1.92298,0 -4.4092,1.44573 -5.76895,0c-1.35976,-1.44573 -2.80525,-3.46245 -3.84597,-6.13384c-0.73591,-1.889 -3.84597,-6.13384 -3.84597,-8.17845c0,-2.04461 -1.92298,-4.08923 -3.84597,-6.13384c-1.92298,-2.04461 -2.48621,-2.6435 -3.84597,-4.08923c-1.35976,-1.44573 -0.49325,-5.71878 -1.92298,-8.17845c-3.19697,-5.50002 -2.80525,-7.55168 -3.84597,-10.22307c-1.47179,-3.77793 -0.88227,-7.55168 -1.92298,-10.22307c-1.47179,-3.77793 0,-6.13384 0,-10.22307c0,-6.13384 0,-10.22307 0,-14.3123c0,-2.04461 2.25584,-1.74349 3.84597,-4.08923c2.5142,-3.70892 3.56279,-6.48775 5.76895,-8.17845c3.48828,-2.67326 5.17943,-7.07191 7.69194,-8.17845c1.7766,-0.78245 2.48621,-0.59888 3.84597,-2.04461c2.71951,-2.89152 7.69194,0 9.61492,0c1.92298,0 7.69194,0 11.53791,0c1.92298,0 5.91534,-0.78245 7.69194,0c2.5125,1.10654 5.76895,4.08923 7.69194,6.13384c1.92298,2.04461 6.43467,3.48704 9.61492,8.17845c2.5142,3.70892 6.05616,7.10355 7.69194,8.17845c3.65774,2.40358 6.5744,11.07946 9.61492,14.3123c3.04052,3.23283 3.84597,8.17845 5.76895,8.17845c1.92298,0 0,-4.08923 0,-6.13384c0,-2.04461 -4.72824,-7.55168 -5.76895,-10.22307c-1.47179,-3.77793 -4.12343,-10.08842 -5.76895,-14.3123c-6.98129,-17.92038 -10.04605,-24.33669 -11.53791,-28.62459c-2.75082,-7.90653 -6.07916,-18.90045 -9.61492,-28.62459c-4.0433,-11.11996 -9.49799,-20.49674 -13.46089,-30.6692c-5.6044,-14.38605 -7.81773,-22.44776 -9.61492,-28.62459c-4.13749,-14.22007 -6.51716,-24.61199 -7.69194,-34.75843c-0.96874,-8.36702 -2.88263,-12.17221 -3.84597,-28.62459c-0.47796,-8.16267 -0.23494,-20.46149 0,-22.49075c0.96874,-8.36702 3.29624,-8.61124 7.69194,-14.3123c1.72413,-2.23611 5.22858,-8.81272 11.53791,-14.3123c5.36192,-4.67376 13.46089,-10.22307 24.9988,-18.40152c5.76895,-4.08923 11.16417,-7.05063 19.22984,-10.22307c7.43619,-2.92478 21.15283,-6.13384 24.9988,-6.13384c7.69194,0 19.22984,0 23.07581,0c7.69194,0 15.68555,3.2299 26.92178,8.17845c3.97261,1.7496 9.74186,7.92831 13.46089,10.22307c5.99677,3.70018 12.97322,12.59726 19.22984,22.49075c5.36503,8.48357 13.37468,17.47974 15.38388,24.53536c1.11448,3.91377 1.14224,17.38808 5.76895,26.57998c1.2832,2.5494 2.37415,10.53436 3.84597,14.3123c1.04072,2.67139 5.76895,16.35691 7.69194,24.53536c1.92298,8.17845 5.50223,16.37669 5.76895,18.40152c1.94176,14.74115 9.14503,20.47677 9.61492,24.53536c0.96877,8.36702 1.92298,10.22307 3.84597,12.26768c1.92298,2.04461 2.85807,6.49418 3.84597,2.04461c0.44184,-1.98989 0,-4.08923 0,-8.17845c0,-2.04461 1.18708,-6.28946 1.92298,-8.17845c1.04072,-2.67139 4.58992,-3.92076 9.61492,-6.13384c1.77662,-0.78245 5.84342,-1.06205 11.53791,-2.04461c6.00246,-1.03566 11.36056,-5.1038 19.22984,-6.13384c5.7257,-0.74945 15.38388,0 19.22984,0c5.76895,0 17.51261,0.1656 24.9988,2.04461c4.18487,1.05039 11.53791,4.08923 13.46089,6.13384c5.76895,6.13384 7.69194,8.17845 9.61492,10.22307c3.84597,4.08923 8.27503,9.75147 9.61492,12.26768c3.90647,7.33591 3.84597,20.44614 3.84597,26.57998c0,6.13384 2.94357,25.15789 0,32.71382c-1.04072,2.67139 -1.92298,6.13384 -1.92298,12.26768l0,2.04461l0,2.04461l0,2.04461" id="svg_2" stroke="#000" fill="none"/>
            </g>
            </svg>
            <p>Current GPU temperature is {}</p>
            <form action="/" method="POST">
                Turn LED :
                <input type="submit" name="submit" value="On">
                <input type="submit" name="submit" value="Off">
            </form>
            </body>
            </html>
        '''
        temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
        self.do_HEAD()
        self.wfile.write(html.format(temp[5:]).encode("utf-8"))

    def do_POST(self):
        """ do_POST() can be tested using curl command 
            'curl -d "submit=On" http://server-ip-address:port' 
        """
        content_length = int(self.headers['Content-Length'])    # Get the size of data
        post_data = self.rfile.read(content_length).decode("utf-8")   # Get the data
        post_data = post_data.split("=")[1]    # Only keep the value
        
        # GPIO setup

        if post_data == 'On':
            print("post_Data ist on")
        else:
            print("post_data ist nicht On")    
        print("LED is {}".format(post_data))
        self._redirect('/')    # Redirect back to the root url



if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
