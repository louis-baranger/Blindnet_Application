from http.server import BaseHTTPRequestHandler, HTTPServer
from os.path import exists


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # extracts needed data
        self.rfile.readline()
        self.rfile.readline()
        self.rfile.readline()
        body = self.rfile.readline()

        current_id = open('maxID.txt').read()
        id_file = open('maxID.txt', 'w')
        id_file.write(str(int(current_id) + 1))
        id_file.close()

        encrypted_file = open(current_id + self.headers['extension'], 'wb')
        encrypted_file.write(body)
        encrypted_file.close()

        file_name = open(current_id + ".txt", 'w')
        file_name.write(self.headers['name'])
        file_name.close()

        self.send_response(200)
        self.end_headers()
        self.wfile.write(current_id.encode('ascii'))

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        message = "ofnhoissg"
        self.wfile.write(bytes(message, "utf8"))
        return


with HTTPServer(('', 8000), SimpleHTTPRequestHandler) as server:
    if not exists('maxID.txt'):
        open('maxID.txt', 'w').write("0")
    server.serve_forever()
