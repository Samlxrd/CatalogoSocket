import socket
import catalogo
import threading
import json

class ServerSocket:
    def __init__(self, HOST, PORT):
        
        self.ADDR = (HOST, PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

        self.clients = []

    def stop_server(self):
        self.server.close()

    def start_server(self):
        print("[!] O Servidor está inicializando...")
        print("[!] LOG Message format: [LOG] [{NOME}]: {MENSAGEM}")
        self.server.listen()

        print(f'[!] Servidor ativo [{self.ADDR[0]}]')

        # Inicializa o Banco de Dados do catálogo caso ele não exista
        self.ctlg = catalogo.Catalogo()
        self.ctlg._criar_tabelas()

        # Se os tipos não tiverem cadastrados, o cadastro é feito.
        # Tipos: (Filme, Serie, Anime, Outro)
        if not self.ctlg.query_types():
            self.ctlg._criar_tipos()

        self.ctlg.close_connection()

        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[*] Conexões ativas: {threading.active_count() - 1}")

    def send_data(self, conn, data):
        message = json.dumps(data)
        conn.send(message.encode())

    def receive_data(self, conn):
        data = conn.recv(1024).decode()
        if data:
            data = json.loads(data)
        return data

    def handle_client(self, conn, addr):
        client_username = ''
        try:
            connected = True

            # Rececbe o nome do usuário
            data = self.receive_data(conn)
            client_username = data['username']
            self.clients.append((conn, client_username))
            
            # Mensagem de LOG
            print(f"[!] [+] ({addr}) {client_username} conectou-se.")

            while connected:

                # Recebe uma ação do cliente
                data = self.receive_data(conn)
                if not data:
                    break
                
                # Conecta ao banco de dados
                db = catalogo.Catalogo()
                print(f'[LOG] ({addr}, {client_username}) : {data}')
            
                # Verifica qual ação foi requisitada ao servidor
                if data['action'] == 'query_all':
                    print('Solicitado query_all')
                    response = {"data":[]}
                    query = db.query_items()

                    for x in query:
                        response['data'].append({'id': x[0], 'nome': x[1], 'tipo': x[2]})
                    
                    print(response)
                    # Enviar json com dados
                    self.send_data(conn, response)

        finally:
            self.clients.remove((conn, client_username))
            print(f'[LOG] Desconectando: ({addr,client_username})')
            conn.close()

def main():
    
    # Define porta e endereço do servidor
    PORT = 5050
    HOST = '127.0.0.1'
    server = ServerSocket(HOST, PORT)
    server.start_server()

if __name__ == "__main__":
    main()