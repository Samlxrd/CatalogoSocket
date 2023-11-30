import socket
import json

class ClientSocket:
    def __init__(self, username, server, port):
        self.addr = (server, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.send_username(username)

    # Conecta ao servidor no endereço informado.
    def connect(self):
        self.client.connect(self.addr)

    # Função responsável por o nome de usuário do cliente para o servidor..
    def send_username(self, username):
        message = json.dumps({'username': username})
        self.client.send(message.encode())

    # Função responsável por enviar dados para o servidor.
    def send_data(self, data):
        message = json.dumps(data)
        self.client.send(message.encode())

    # Função responsável por receber dados do servidor.
    def receive_data(self):
        data = self.client.recv(1024).decode()
        print('Recebido no cliente:\n', data)
        data = json.loads(data)
        return data
    
    # Encerra conexão com o servidor.
    def close_connection(self):
        self.client.close()