import urlparse
import cgi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from nif import Wrapper

PORT = 8001

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        This method receives a GET request and handles it.
        """
        if self.path.startswith("/service"):
            path = urlparse.parse_qs(self.path.split("?")[1])

            input_text, options = self.qs2options(path)

            self.response(input_text, options)
        else:
            self.send_error(404, "File not found")

    def do_POST(self):
        """
        This method receives a POST request and handles it.
        """
        if self.path.startswith("/service"):
            length = int(self.headers.getheader('content-length'))
            qs = self.rfile.read(length)
            para = cgi.parse_qs(qs, keep_blank_values=1)

            input_text, options = self.qs2options(para)
            
            self.response(input_text, para)
        else:
            self.send_error(404, "File not found")

    def response(self, input_text, options):
        """
        This method proceeds the given operation and returns
        a HTTP response.
        """
        wrapper = Wrapper(input_text, options)
        rdf = wrapper.nlp2rdf()
        self.send_response(200)
        if options.get('format') == "n3":
            self.send_header('Content-type','text/n3')
        elif options.get('format') == "ntriples":
            self.send_header('Content-type','text/plain')
        elif options.get('format') == "turtle":
            self.send_header('Content-type','text/turtle')
        else:
            self.send_header('Content-type','application/rdf+xml')
        self.end_headers()
        self.wfile.write(rdf)

    def qs2options(self, qs):
        """
        Converts a query string dictionary into a
        modified options dictionary.
        """
        try:
            input_type = qs["input-type"][0]
            input_text = qs["input"][0]
        except KeyError:
            self.send_error(500, "Missed required parameters")

        options = {
            'nif': qs.get('nif'),
            'format': qs.get('format'),
            'prefix': qs.get('prefix'),
            'urirecipe': qs.get('offset')
            }
        
        return (input_text, options)

if __name__ == "__main__":
    try:
        server = HTTPServer(('', PORT), MyHandler)
        print "server running at", PORT
        server.serve_forever()
    except KeyboardInterrupt:
        print "bye bye.."
        server.socket.close()
