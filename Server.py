from http.server import BaseHTTPRequestHandler, HTTPServer
from os.path import exists
import shutil


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

        metadata = open(current_id + ".txt", 'w')
        metadata.write(self.headers['name'])
        metadata.write('\n')
        metadata.write(self.headers['extension'])
        metadata.write('\n')
        metadata.write(self.headers['salt'])
        metadata.write('\n')
        metadata.write(self.headers['type'])
        metadata.close()

        self.send_response(200)
        self.end_headers()
        self.wfile.write(current_id.encode('ascii'))

    def do_GET(self):
        if exists(self.headers['id'] + '.txt'):
            self.get_file()
            self.end_headers()
        else:
            self.send_response(201)
            self.end_headers()
            message = "File not found."
            self.wfile.write(message.encode('ascii'))

        return

    def get_file(self):
        metadata = open(self.headers['id'] + '.txt', 'r')
        name = str(metadata.readline()[:-1])
        extension = str(metadata.readline()[:-1])
        salt = str(metadata.readline()[:-1])
        type_send = str(metadata.readline())
        metadata.close()

        self.send_response(200)
        headers = {'name': name, 'extension': extension, 'salt': salt, 'type_send': type_send}
        self.send_header('name', name)
        self.send_header('extension', extension)
        self.send_header('salt', salt)
        self.send_header('type_send', type_send)
        self.end_headers()

        with open(self.headers['id'] + extension, 'rb') as content:
            shutil.copyfileobj(content, self.wfile)

        return


with HTTPServer(('', 8000), SimpleHTTPRequestHandler) as server:
    if not exists('maxID.txt'):
        open('maxID.txt', 'w').write("0")
    server.serve_forever()
