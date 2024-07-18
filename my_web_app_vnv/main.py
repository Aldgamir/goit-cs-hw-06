import http.server
import socketserver
import socket
import threading
import json
import os
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from http import HTTPStatus

# Шлях до статичних файлів
STATIC_DIR = './static'

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/':
            self.path = 'index.html'
        elif parsed_path.path == '/message':
            self.path = 'message.html'
        elif self.path.startswith('/static/'):
            self.path = self.path[1:]
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return

        return super().do_GET()

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/submit':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode('utf-8'))
            username = data['username'][0]
            message = data['message'][0]
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

            # Відправка даних на Socket-сервер
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', 5000))
            sock.sendall(json.dumps({
                'date': timestamp,
                'username': username,
                'message': message
            }).encode('utf-8'))
            sock.close()

            self.send_response(HTTPStatus.SEE_OTHER)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")

def run_http_server():
    PORT = 3000
    handler = MyHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    print(f"HTTP server running on port {PORT}")
    httpd.serve_forever()

if __name__ == '__main__':
    threading.Thread(target=run_http_server).start()