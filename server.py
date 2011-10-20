import urlparse
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer

from nif import Wrapper

PORT = 8001

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/service"):
            path = urlparse.parse_qs(self.path.split("?")[1])
            try:
                input_type = path["input-type"]
                input_text = path["input"][0]
            except KeyError:
                self.send_error(500, "Missed required parameters")

            options = {
                'nif': path.get('nif'),
                'format': path.get('format'),
                'prefix': path.get('prefix'),
                'urirecipe': path.get('offset')
                }

            # proceed tagging
            wrapper = Wrapper(input_text, options)
            rdf = wrapper.nlp2rdf()
            self.send_response(200)
            if options.get('format')[0] == "n3":
                self.send_header('Content-type','text/html')
            # TODO more MIME types
            else:
                self.send_header('Content-type','application/rdf+xml')
            self.end_headers()
            self.wfile.write(rdf)
        else:
            self.send_error(404, "File not found")

if __name__ == "__main__":
    try:
        server = HTTPServer(('', PORT), MyHandler)
        print "server running at", PORT
        server.serve_forever()
    except KeyboardInterrupt:
        print "bye bye.."
        server.socket.close()
