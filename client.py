import socket
import json

class ClientSocket:
    def __init__(self, server, port):
        self.addr = (server, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        self.client.connect(self.addr)

    def send_data(self, data):
        message = json.dumps(data)
        self.client.send(message.encode())

    def receive_data(self):
        data = self.client.recv(1024).decode()
        return {'Resultado da Consulta'}

    def search_data(data):
        return {'Resultado da Consulta'}

    def add_data(data):
        return {'Resultado da Consulta'}
    
    def query_favourites(data):
         #send_data(self, data):
         #receive_data
         #tratar resposta
        return {'Resultado da Consulta'}

    def edit_data(data_id, new_data):
        return {'Resultado da Consulta'}

    def delete_data(data_id):
        return {'Resultado da Consulta'}
    
    def close_connection(self):
        self.client.close()

# Como será feita a chamada
PORT = 5050
SERVER = '127.0.0.1'
client_socket = ClientSocket(SERVER, PORT)

