import socket
import threading
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse
import datetime
import json

# Путь к папке с HTML и статическими файлами
WEB_DIR = os.path.join(os.path.dirname(__file__), 'web')

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/message':
            self.path = '/message.html'
        
        try:
            file_path = os.path.join(WEB_DIR, self.path[1:])
            if os.path.isfile(file_path):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_error(404, 'File Not Found')
        except Exception as e:
            self.send_error(500, 'Internal Server Error')

    def do_POST(self):
        if self.path == '/submit':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            
            message_data = {
                "date": str(datetime.datetime.now()),
                "username": parsed_data.get('username', [''])[0],
                "message": parsed_data.get('message', [''])[0]
            }
            
            # Відпрвляємо фійли на Socket-сервер
            send_to_socket_server(message_data)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Message received')
        else:
            self.send_error(404, 'Not Found')

def run_http_server():
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, CustomHandler)
    print("HTTP Server running on port 3000")
    httpd.serve_forever()

def send_to_socket_server(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 5000))
    sock.sendall(json.dumps(data).encode('utf-8'))
    sock.close()

# Запускаємо HTTP сервер в окремому потоці
http_server_thread = threading.Thread(target=run_http_server)
http_server_thread.start()