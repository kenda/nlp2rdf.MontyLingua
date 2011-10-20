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
                'nif': None,
                'format': None,
                'prefix': None,
                'urirecipe': None
                }

            # proceed tagging
            wrapper = Wrapper()
            text = wrapper.pos_tag(input_text)
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(text)
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
