import socket
import threading
import json
from pymongo import MongoClient
from datetime import datetime

# Настройки MongoDB
client = MongoClient('mongodb://mongo:27017/')
db = client.message_db
collection = db.messages

def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    data = json.loads(request.decode('utf-8'))
    collection.insert_one(data)
    client_socket.close()

def run_socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))
    server.listen(5)
    print("Socket server працбьє на порті 5000")
    while True:
        client_sock, address = server.accept()
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,)
        )
        client_handler.start()

if __name__ == '__main__':
    run_socket_server()