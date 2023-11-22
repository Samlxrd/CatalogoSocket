import socket
import json

class ClientSocket:
    def __init__(self, username, server, port):
        self.addr = (server, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.send_username(username)

    def connect(self):
        self.client.connect(self.addr)

    def send_username(self, username):
        message = json.dumps({'username': username})
        self.client.send(message.encode())

    def send_data(self, data):
        message = json.dumps(data)
        self.client.send(message.encode())

    def receive_data(self):
        data = self.client.recv(1024).decode()
        print('Recebido no cliente:\n', data)
        data = json.loads(data)
        return data
    
    def close_connection(self):
        self.client.close()