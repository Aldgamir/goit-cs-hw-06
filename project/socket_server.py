import socket
import threading
import json
from pymongo import MongoClient
import datetime

client = MongoClient('mongodb://mongo:27017/')
db = client['messages_db']
collection = db['messages']

def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    message_data = json.loads(request.decode('utf-8'))
    collection.insert_one(message_data)
    client_socket.close()

def run_socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))
    server.listen(5)
    print("Socket Server running on port 5000")

    while True:
        client_sock, address = server.accept()
        client_handler = threading.Thread(target=handle_client_connection, args=(client_sock,))
        client_handler.start()

# Запускаємо Socket сервера
run_socket_server()